#!/bin/sh

newIpEnd0=$1
newIpWlan0=$2
echo "Changing virtual ip for end0 to ${newIpEnd0}..."
sed -i "s/^virtual_ip_end0=.*/virtual_ip_end0='${newIpEnd0}'/" /var/www/html/openWB/openwb.conf
echo "Changing virtual ip for wlan0 to ${newIpWlan0}..."
sed -i "s/^virtual_ip_wlan0=.*/virtual_ip_wlan0='${newIpWlan0}'/" /var/www/html/openWB/openwb.conf
echo "done"
