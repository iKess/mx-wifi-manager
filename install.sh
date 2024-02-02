sudo mv mx-wifi-manager.service /etc/systemd/system/
sudo mv *.py /usr/local/myssix/wifi-manager/

sudo systemctl enable mx-wifi-manager.service
sudo systemctl start mx-wifi-manager.service
