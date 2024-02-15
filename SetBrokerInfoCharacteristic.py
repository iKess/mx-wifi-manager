from pybleno import *
import array
import sys
import subprocess
import re

class SetBrokerInfoCharacteristic(Characteristic):
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': '2CBA',
            'properties': ['write'],
            'value': None,
            'descriptors': [
                  Descriptor({
                    'uuid': '2CBA',
                    'value': 'MySmaX Broker IP:Port'
                  }),
            ]
          })
          
        self._value = array.array('L', [0] * 0)
        self._updateValueCallback = None
        
    def onWriteRequest(self, data, offset, withoutResponse, callback):
        
        print('[brokerInfo] Write request: value = ' + str(data) + ' offset = ' + str(offset) + ' withoutResponse = ' + str(withoutResponse))
        brokerInfo = data.decode()
        # addWifi(ssid, pw)
        with open('/var/tmp/mx-broker.txt', 'w') as file:
            file.write(brokerInfo)
        print('The file has been saved!')
        
        if brokerInfo and brokerInfo.has(':'):
            print('Broker IP:Port is set to ' + brokerInfo)
            callback(Characteristic.RESULT_SUCCESS)
        else:
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
        
        