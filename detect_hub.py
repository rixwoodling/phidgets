from Phidget22.Devices.DigitalInput import DigitalInput
from Phidget22.Phidget import Phidget
from Phidget22.PhidgetException import PhidgetException

hub = DigitalInput()

# Find any Phidget hub
hub.setDeviceSerialNumber(Phidget.ANY_SERIAL_NUMBER)

# VINT port 0
hub.setHubPort(0)

# Port itself, rather than a VINT device attached to it
hub.setIsHubPortDevice(True)

try:
    hub.openWaitForAttachment(5000)

    print("Attached!")
    print("Device:", hub.getDeviceName())
    print("Device class:", hub.getDeviceClassName())
    print("SKU:", hub.getDeviceSKU())
    print("Serial:", hub.getDeviceSerialNumber())
    print("Hub port:", hub.getHubPort())
    print("Channel:", hub.getChannel())

finally:
    hub.close()
