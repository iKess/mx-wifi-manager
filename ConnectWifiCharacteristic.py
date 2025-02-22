from pybleno import *
import array
import sys
import subprocess
import re

ssid = ''
pw = ''

def get_wifi_ip_address():
    result = subprocess.run(['ifconfig', 'wlan0'], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')

    ip_address_match = re.search(r'inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', result)
    if ip_address_match:
        return ip_address_match.group(1)
    else:
        return None


def check_wifi_connection():
    result = subprocess.run(['iwconfig'], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')

    if 'ESSID:off/any' in result:
        print('Not connected to any network')
    else:
        ssid = re.search('ESSID:"(.+?)"', result)
        if ssid:
            print('Connected to network:', ssid.group(1))
        else:
            print('Could not determine network')

def switch_wifi_network(ssid, passphrase):
    
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as wifi_file:
        wifi_file.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
        wifi_file.write('update_config=1\n')
        wifi_file.write('country=KR\n')
        wifi_file.write('\nnetwork={\n')
        wifi_file.write('    ssid="{}"\n'.format(ssid))
        wifi_file.write('    psk="{}"\n'.format(passphrase))
        wifi_file.write('}\n')

    subprocess.call(['sudo', 'systemctl', 'daemon-reload'])
    subprocess.call(['sudo', 'systemctl', 'restart', 'wpa_supplicant'])
    # subprocess.call(['sudo', 'reboot']) 

def connect_to_wifi(ssid, passphrase):
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a') as wifi_file:
        wifi_file.write('\nnetwork={\n')
        wifi_file.write('    ssid="{}"\n'.format(ssid))
        wifi_file.write('    psk="{}"\n'.format(passphrase))
        wifi_file.write('}\n')

    subprocess.call(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'])
    
class ConnectWifiCharacteristic(Characteristic):
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': '2ABC',
            'properties': ['write'],
            'value': None,
            'descriptors': [
                  Descriptor({
                    'uuid': '2ABC',
                    'value': 'Connect Wifi with SSID, PW'.encode('utf-8')
                  }),
            ]
          })
          
        self._value = array.array('L', [0] * 0)
        self._updateValueCallback = None
        
    def onWriteRequest(self, data, offset, withoutResponse, callback):
        global ssid, pw
        print('Write request: value = ' + str(data) + ' offset = ' + str(offset) + ' withoutResponse = ' + str(withoutResponse))
        
        if (ssid == '' or pw == ''): 
            print('SSID or PW is empty')
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
        
        check_wifi_connection()
        
        ip_address = get_wifi_ip_address()
        if ip_address:
            print('IP address:', ip_address)
            switch_wifi_network(ssid, pw)
        else:
            print('Could not determine IP address')
            connect_to_wifi(ssid, pw)
        
        callback(Characteristic.RESULT_SUCCESS)
          
class SetSSIDCharacteristic(Characteristic):
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': '2ABD',
            'properties': ['write'],
            'value': None,
            'descriptors': [
                  Descriptor({
                    'uuid': '2ABD',
                    'value': 'Wifi SSID'.encode('utf-8')
                  }),
            ]
          })
          
        self._value = array.array('L', [0] * 0)
        self._updateValueCallback = None
        
    def onWriteRequest(self, data, offset, withoutResponse, callback):
        global ssid
        
        print('Write request: value = ' + str(data) + ' offset = ' + str(offset) + ' withoutResponse = ' + str(withoutResponse))
        ssid = data.decode()
        # addWifi(ssid, pw)
        check_wifi_connection()
        
        callback(Characteristic.RESULT_SUCCESS)
        
class SetPWCharacteristic(Characteristic):
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': '2ABF',
            'properties': ['write'],
            'value': None,
            'descriptors': [
                  Descriptor({
                    'uuid': '2ABF',
                    'value': 'Wifi Passphrase'.encode('utf-8')
                  }),
            ]
          })
          
        self._value = array.array('L', [0] * 0)
        self._updateValueCallback = None
        
    def onWriteRequest(self, data, offset, withoutResponse, callback):
        global pw
        
        print('Write request: value = ' + str(data) + ' offset = ' + str(offset) + ' withoutResponse = ' + str(withoutResponse))
        pw = data.decode()
        # addWifi(ssid, pw)
        check_wifi_connection()
        
        callback(Characteristic.RESULT_SUCCESS)
