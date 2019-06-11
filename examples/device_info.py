# Example of displaying the device information service (DIS) info for a UART device.
#
# !!! NOTE !!!
#
# Only works on Mac OSX at this time.  On Linux bluez appears to hide the DIS
# service entirely. :(
#
# !!! NOTE !!!
#
# Author: Tony DiCola
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART, DeviceInformation


# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()


# Main function implements the program logic so it can run in a background
# thread.  Most platforms require the main thread to handle GUI events and other
# asyncronous events like BLE actions.  All of the threading logic is taken care
# of automatically though and you just need to provide a main function that uses
# the BLE provider.
def main():
    # Clear any cached data because both bluez and CoreBluetooth have issues with
    # caching data and it going stale.
    ble.clear_cached_data()

    # Get the first available BLE network adapter and make sure it's powered on.
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    # Disconnect any currently connected UART devices.  Good for cleaning up and
    # starting from a fresh state.
    print('Disconnecting any connected UART devices...')
    UART.disconnect_devices()

    # Scan for UART devices.
    print('Searching for UART device...')
    try:
        adapter.start_scan()
        # Search for the first UART device found (will time out after 60 seconds
        # but you can specify an optional timeout_sec parameter to change it).
        device = UART.find_device()
        if device is None:
            raise RuntimeError('Failed to find UART device!')
    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

    print('Connecting to device...', device.name)
    device.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
                      # to change the timeout.
                      
    

    # Once connected do everything else in a try/finally to make sure the device
    # is disconnected when done.
    try:
        # Wait for service discovery to complete for the DIS service.  Will
        # time out after 60 seconds (specify timeout_sec parameter to override).
        print('Discovering services...')
        DeviceInformation.discover(device)
        
        
        s_start = 'S01'
        s_stop = 'S00'
        
        
        s_unkn1 = 'DR0401'
        s_unkn2 = 'DW0308'
        
        

        
        
        import uuid
        
        u = uuid.UUID('00002902-0000-1000-8000-00805f9b34fb')
        
        d = uuid.UUID('00002902-0000-1000-8000-00805f9b34fb')
        e = uuid.UUID('6e400001-b5a3-f393-e0a9-e50e24dcca9e')
        f = uuid.UUID('6e400002-b5a3-f393-e0a9-e50e24dcca9e')
        g = uuid.UUID('6e400003-b5a3-f393-e0a9-e50e24dcca9e')
        
        
        
        def val_change_cb(val):
            print("val_change_cb:", val)
        
        s = device.list_services()[0]
        print("service:", s.uuid)
        
        gg = s.find_characteristic(g)
        print("find characteristic:", gg, "for g:", g)
        dd = gg.find_descriptor(d)
        print("find descriptor:", dd, "for d:", d)
        # gg.start_notify(val_change_cb)
        # dd.start_notify(val_change_cb)
        
        ff = s.find_characteristic(f)
        print("find characteristic:", ff, "for f:", f)
        dr = 'S01'.encode(encoding='UTF-8')
        ff.write_value(dr)
        print("sent dr:", dr, "to f:", f)
        
        
        print("gg value:", gg.read_value())
        
        
        # 
        # characteristics = s.list_characteristics()
        # for characteristic in characteristics:
        #     
        #     print("charact:", characteristic.uuid)
        #     desc = characteristic.list_descriptors()
        #     characteristic.write_value(str(s.uuid))
        #     characteristic.start_notify(f)
        #     print(desc)
        #     for d in desc:
        #         print("desc:", d.uuid)
        #         
        #     #print(characteristic.find_descriptor(u))
        #     
        #     #print("list desc:")
        #     #print(characteristic.list_descriptors())
        #     
        #     # print(characteristic.read_value())
        #     dr = 'DR0401'.encode(encoding='UTF-8')
        #     characteristic.write_value(dr)
        #     
        #     



        
        # 
        # # import time
        # # print('Waiting 60 seconds to receive data from the device...')
        # # time.sleep(60)
        # import time
        # while True:
        #     
        #     # print('Waiting 60 seconds to receive data from the device...')
        #     time.sleep(5)
        #     
        #     
            
        
        raw_input("Press any key to quit...")
        
    except IOError as (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
    except ValueError:
        print "Could not convert data to an integer."
    except:
        import sys
        print "Unexpected error:", sys.exc_info()[0]
        raise
    
    finally:
        pass
        # Make sure device is disconnected on exit.
        # device.disconnect()


# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)
