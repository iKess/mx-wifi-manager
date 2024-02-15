# mx-wifi-manager

sudo cp systemd-services/mx-device-wifi-manager.service /etc/systemd/system/mx-device-wifi-manager.service

sudo mkdir -p /usr/local/myssix/wifi-manager
sudo cp *.py /usr/local/myssix/wifi-manager

sudo vi /etc/wpa_supplicant/wpa_supplicant.conf 
sudo vi /etc/network/interfaces

sudo service mx-device-wifi-manager status
sudo service mx-device-wifi-manager start
sudo service mx-device-wifi-manager restart

### useful commands

iwconfig

sudo systemctl status mx-wifi-manager
sudo wpa_cli -i wlan0 reconfigure
sudo systemctl restart wpa_supplicant
sudo systemctl status dhcpcd
sudo raspi-config
sudo systemctl restart network-manager