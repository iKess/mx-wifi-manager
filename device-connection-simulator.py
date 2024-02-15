from pybleno import *
import sys
import signal
from DeviceWifiService import *
from HubWifiService import *
import asyncio 



bleno = Bleno()

deviceService = DeviceWifiService()
hubService = HubWifiService()

def onStateChange(state):
   print('on -> stateChange: ' + state)

   if (state == 'poweredOn'):
       bleno.startAdvertising('MXWifiManager', [deviceService.uuid])
   else:
     bleno.stopAdvertising()
bleno.on('stateChange', onStateChange)

def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'));

    if not error:
        def on_setServiceError(error):
            print('setServices: %s'  % ('error ' + error if error else 'success'))
            
        bleno.setServices([
            hubService,
            deviceService
        ], on_setServiceError)
bleno.on('advertisingStart', onAdvertisingStart)

bleno.start()

# print ('Hit <ENTER> to disconnect')

# if (sys.version_info > (3, 0)):
#     input()
# else:
#     raw_input()

loop = asyncio.get_event_loop()
try:
    loop.run_forever()
finally:
    loop.close()
    bleno.stopAdvertising()
    bleno.disconnect()

print ('terminated.')
sys.exit(1)
