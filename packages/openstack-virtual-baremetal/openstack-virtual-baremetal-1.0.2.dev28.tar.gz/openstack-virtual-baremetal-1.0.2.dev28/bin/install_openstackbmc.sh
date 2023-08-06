#!/bin/bash
set -x

# Also python-crypto, but that requires special handling because we used to
# install python2-crypto from EPEL
# python-[nova|neutron]client are in a similar situation.  They were renamed
# in RDO to python2-*
required_packages="python-pip os-net-config git jq python2-os-client-config python2-openstackclient"

function have_packages() {
    for i in $required_packages; do
        if ! rpm -qa | grep -q $i; then
            return 1
        fi
    done
    if ! (rpm -qa | egrep -q "python-crypto|python2-crypto"); then
        return 1
    fi
    if ! (rpm -qa | egrep -q "python-novaclient|python2-novaclient"); then
        return 1
    fi
    if ! (rpm -qa | egrep -q "python-neutronclient|python2-neutronclient"); then
        return 1
    fi
    if ! pip freeze | grep -q pyghmi; then
        return 1
    fi
    return 0
}

if ! have_packages; then
    yum install -y wget
    wget -r --no-parent -nd -e robots=off -l 1 -A 'python2-tripleo-repos-*' https://trunk.rdoproject.org/centos7/current/
    yum install -y python2-tripleo-repos-*
    tripleo-repos current-tripleo
    yum install -y $required_packages python-crypto python2-novaclient python2-neutronclient
    pip install pyghmi
fi

cat <<EOF >/usr/local/bin/openstackbmc
$openstackbmc_script
EOF
chmod +x /usr/local/bin/openstackbmc

# Configure clouds.yaml so we can authenticate to the host cloud
mkdir -p ~/.config/openstack
# Passing this as an argument is problematic because it has quotes inline that
# cause syntax errors.  Reading from a file should be easier.
cat <<'EOF' >/tmp/bmc-cloud-data
$cloud_data
EOF
python -c 'import json
import sys
import yaml
with open("/tmp/bmc-cloud-data") as f:
    data=json.loads(f.read())
clouds={"clouds": {"host_cloud": data}}
print(yaml.safe_dump(clouds, default_flow_style=False))' > ~/.config/openstack/clouds.yaml
rm -f /tmp/bmc-cloud-data
export OS_CLOUD=host_cloud

private_subnet=$(openstack network show -f value -c subnets $private_net)
default_gw=$(openstack subnet show -f value -c gateway_ip $private_subnet)
prefix_len=$(openstack subnet show -f value -c cidr $private_subnet | awk -F / '{print $2}')
cache_status=
if [ "$bmc_use_cache" != "False" ]; then
    cache_status="--cache-status"
fi

mkdir /etc/os-net-config
echo "network_config:" > /etc/os-net-config/config.yaml
echo "  -" >> /etc/os-net-config/config.yaml
echo "    type: interface" >> /etc/os-net-config/config.yaml
echo "    name: eth0" >> /etc/os-net-config/config.yaml
echo "    use_dhcp: false" >> /etc/os-net-config/config.yaml
echo "    mtu: 1450" >> /etc/os-net-config/config.yaml
echo "    routes:" >> /etc/os-net-config/config.yaml
echo "      - default: true" >> /etc/os-net-config/config.yaml
echo "        next_hop: $default_gw" >> /etc/os-net-config/config.yaml
echo "    addresses:" >> /etc/os-net-config/config.yaml
echo "    - ip_netmask: $bmc_utility/$prefix_len" >> /etc/os-net-config/config.yaml

cat <<EOF >/usr/lib/systemd/system/config-bmc-ips.service
[Unit]
Description=config-bmc-ips Service
Requires=network.target
After=network.target

[Service]
ExecStart=/bin/os-net-config --verbose
Type=oneshot
User=root
StandardOutput=kmsg+console
StandardError=inherit

[Install]
WantedBy=multi-user.target
EOF

for i in $(seq 1 $bm_node_count)
do
    bm_port="$bm_prefix_$(($i-1))"
    bm_instance=$(openstack port show -c device_id -f value $bm_port)
    bmc_port="$bmc_prefix_$(($i-1))"
    bmc_ip=$(openstack port show -c fixed_ips -f value $bmc_port | awk -F \' '{print $2}')
    unit="openstack-bmc-$bm_port.service"

    cat <<EOF >/usr/lib/systemd/system/$unit
[Unit]
Description=openstack-bmc $bm_port Service
Requires=config-bmc-ips.service
After=config-bmc-ips.service

[Service]
ExecStart=/usr/local/bin/openstackbmc  --os-cloud host_cloud --instance $bm_instance --address $bmc_ip $cache_status
Restart=always

User=root
StandardOutput=kmsg+console
StandardError=inherit

[Install]
WantedBy=multi-user.target
EOF

    echo "    - ip_netmask: $bmc_ip/$prefix_len" >> /etc/os-net-config/config.yaml
done

# It will be automatically started because the bmc services depend on it,
# but to avoid confusion also explicitly enable it.
systemctl enable config-bmc-ips

for i in $(seq 1 $bm_node_count)
do
    bm_port="$bm_prefix_$(($i-1))"
    unit="openstack-bmc-$bm_port.service"
    systemctl enable $unit
    systemctl start $unit
done

sleep 5

for i in $(seq 1 $bm_node_count)
do
    bm_port="$bm_prefix_$(($i-1))"
    unit="openstack-bmc-$bm_port.service"
    if ! systemctl status $unit
    then
        $signal_command --data-binary '{"status": "FAILURE"}'
        echo "********** $unit failed to start **********"
        exit 1
    fi
done

$signal_command --data-binary '{"status": "SUCCESS"}'

