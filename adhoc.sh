#!/bin/bash

if [ "$(id -u)" != "0" ]
then
	echo "You need to run this with sudo."
	exit 1
fi

dhcpcd='/etc/dhcpcd.conf'
interfaces='/etc/network/interfaces'
hostapd='/etc/hostapd/hostapd.conf'
hostapdd='/etc/default/hostapd'
dnsmasq='/etc/dnsmasq.conf'
rclocal='/etc/rc.local'

# take care of deny interfaces either not being there
# or commented out
if ! grep 'denyinterfaces wlan0' $dhcpcd
then
	echo -e "\ndenyinterfaces wlan0" >> $dhcpcd
else
	sed -i 's/# *\(denyinterfaces wlan0\)/\1/' $dhcpcd
fi

sed -i 's/\(iface wlan0 inet\).*/\1 static/' $interfaces

if ! grep '172.24.1.1' $interfaces
then
	awk '/iface wlan0 inet static/{print $0 RS "\taddress\t\t172.24.1.1" RS "\tnetmask\t\t255.255.255.0" RS "\tnetwork\t\t172.24.1.0" RS "\tbroadcast\t172.24.1.255";next}1' $interfaces > tmp && mv tmp $interfaces
fi

if grep 'UCInet Mobile Access' $interfaces
then
	sed -ie '/UCInet Mobile Access/,+3d' $interfaces
fi

service dhcpcd restart

touch $hostapd

echo -e "interface=wlan0\ndriver=nl80211\nssid=JPi2\nhw_mode=g\nchannel=6\nieee80211n=1\nwmm_enabled=1\nht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0\nwpa=2\nwpa_key_mgmt=WPA-PSK\nwpa_passphrase=raspberry\nrsn_pairwise=CCMP" > $hostapd

sed -i 's:#DAEMON_CONF="":DAEMON_CONF="/etc/hostapd/hostapd.conf":' $hostapdd

mv $dnsmasq $dnsmasq.orig
touch $dnsmasq
echo -e "interface=wlan0\nlisten-address=172.24.1.1\nbind-interfaces\nserver=8.8.8.8\ndomain-needed\nbogus-priv\ndhcp-range=172.24.1.50,172.24.1.150,12h" > $dnsmasq

sed -i 's/# *\(net.ipv4.ip_forward=1\)/\1/' $dhcpcd

iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

sh -c "iptables-save > /etc/iptables.ipv4.nat"

sed -i '/exit 0/i iptables-restore < /etc/iptables.ipv4.nat' $rclocal

service hostapd start
service dnsmasq start

reboot
