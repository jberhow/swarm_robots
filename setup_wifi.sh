#!/bin/bash

if [ "$(id -u)" != "0" ]
then
	echo "You need to run this with sudo."
	exit 1
fi

interfaces='/etc/network/interfaces'
dhcpcd='/etc/dhcpcd.conf'
dnsmasq='/etc/dnsmasq.conf'
rclocal='/etc/rc.local'

# write in murican
setxkbmap us

# wlan1 doesn't even exist... delete it and the next 3 lines
sed -ie '/wlan1/,+3d' $interfaces

# remove wpa supplicant stuff. Might have to rethink this
sed -ie '/iface wlan0 inet manual/,+2d' $interfaces

# add auto wlan0
if ! grep 'auto wlan0' $interfaces
then
	sed -ie '/iface eth0 inet dhcp/a auto wlan0' $interfaces
fi

# replace manual with dhcp cause pi says so
sed -i 's/\(iface eth0 inet\).*/\1 dhcp/' $interfaces
sed -i 's/\(iface wlan0 inet\).*/\1 dhcp/' $interfaces

# add wifi info
if ! grep 'UCInet Mobile Access' $interfaces
then
	echo -e 'iface wlan0 inet dhcp\n\twpa-ssid "UCInet Mobile Access"\n\twpa-key-mgmt NONE\n\twpa-auth-alg OPEN\n' >> $interfaces
fi

if grep 'address' $interfaces
then
	sed -ie '/address/,+4d' $interfaces
fi

sed -i 's/\(denyinterfaces wlan0\)/# \1/' $dhcpcd

sed -ie '/iptables-restore/,+1d' $rclocal

cp $dnsmasq.orig $dnsmasq

service hostapd stop
service dnsmasq stop

reboot
