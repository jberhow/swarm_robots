#!/bin/bash

if [ "$(id -u)" != "0" ]
then
echo "You need to run this with sudo."
exit 1
fi

interfaces='/etc/network/interfaces'

# write in murican
setxkbmap us

# wlan1 doesn't even exist... delete it and the next 3 lines
sed -e '/wlan1/,+3d' < $interfaces > $interfaces.new; \
mv $interfaces.new $interfaces

# remove wpa supplicant stuff. Might have to rethink this
sed -e '/iface wlan0 inet manual/,+2d' < $interfaces > $interfaces.new; \
mv $interfaces.new $interfaces

# add auto wlan0
if ! grep 'auto wlan0' $interfaces
then
sed -e '/iface eth0 inet dhcp/a auto wlan0' < $interfaces > $interfaces.new; \
mv $interfaces.new $interfaces
fi

# replace manual with dhcp cause pi says so
sed 's/\(iface eth0 inet\).*/\1 dhcp/' < $interfaces > $interfaces.new; \
mv $interfaces.new $interfaces

# add wifi info
if ! grep '4SXF5' $interfaces
then
echo -e 'iface wlan0 inet dhcp\n\twpa-ssid "4SXF5"\n\twpa-psk "JL2LH95CNS8Y9PG7"' >> $interfaces
fi

reboot
