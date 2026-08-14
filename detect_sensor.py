from Phidget22.Devices.Manager import Manager
import time


def on_attach(manager, channel):
    print("ATTACHED")
    print(f"  Device:       {channel.getDeviceName()}")
    print(f"  Device class: {channel.getDeviceClassName()}")
    print(f"  Device ID:    {channel.getDeviceID()}")
    print(f"  SKU:          {channel.getDeviceSKU()}")
    print(f"  Serial:       {channel.getDeviceSerialNumber()}")
    print(f"  Hub port:     {channel.getHubPort()}")
    print(f"  Channel:      {channel.getChannel()}")
    print(f"  Channel class:{channel.getChannelClassName()}")
    print()


def on_detach(manager, channel):
    print("DETACHED")
    print(f"  Device: {channel.getDeviceName()}")
    print()


manager = Manager()

manager.setOnAttachHandler(on_attach)
manager.setOnDetachHandler(on_detach)

manager.open()

print("Scanning for Phidgets...")
print("Ctrl-C to exit")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    manager.close()
