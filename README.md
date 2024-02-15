# mx-wifi-manager

cp systemd-services/mx-hub-wifi-manager.service /etc/systemd/system/mx-hub-wifi-manager.service
cp systemd-services/mx-device-wifi-manager.service /etc/systemd/system/mx-device-wifi-manager.service

mkdir -p /usr/local/myssix/wifi-manager
cp *.py /usr/local/myssix/wifi-manager

sudo vi /etc/wpa_supplicant/wpa_supplicant.conf 
sudo vi /etc/network/interfaces

### useful commands

iwconfig

sudo reboot

sudo systemctl status mx-wifi-manager

sudo wpa_cli -i wlan0 reconfigure
sudo systemctl restart wpa_supplicant

sudo systemctl status dhcpcd

sudo raspi-config

sudo systemctl restart network-manager