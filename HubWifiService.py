from pybleno import *
from SetWifiInfoCharacteristic import *
from ConnectWifiCharacteristic import *
    
# class SSIDPasswordCharacteristic(Characteristic):
#     def __init__(self):
#         Characteristic.__init__(self, {
#             'uuid': '0000180a-0000-1000-8000-111111111111',
#             'properties': ['read', 'write'],
#             'value': None
#         })

#     def onReadRequest(self, offset, callback):
#         callback(Characteristic.RESULT_SUCCESS, array.array('b', data))


class HubWifiService(BlenoPrimaryService):
    def __init__(self):
        BlenoPrimaryService.__init__(self, {
          'uuid': '540F',
          'characteristics': [
              ConnectWifiCharacteristic(),
              SetSSIDCharacteristic(),
              SetPWCharacteristic()
          ]})