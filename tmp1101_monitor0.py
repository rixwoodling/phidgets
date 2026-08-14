#!/usr/bin/env python3

import time
from Phidget22.Phidget import Phidget
from Phidget22.Devices.TemperatureSensor import TemperatureSensor
from Phidget22.Devices.VoltageInput import VoltageInput
from Phidget22.ThermocoupleType import ThermocoupleType

# Find the first TemperatureSensor channel on any Phidget
temp = TemperatureSensor()
temp.setDeviceSerialNumber(Phidget.ANY_SERIAL_NUMBER)
temp.setHubPort(Phidget.ANY_HUB_PORT)
temp.setChannel(0)
temp.openWaitForAttachment(5000)

serial = temp.getDeviceSerialNumber()
port = temp.getHubPort()

temp.setThermocoupleType(ThermocoupleType.THERMOCOUPLE_TYPE_K)

# Same physical TMP1101, raw voltage channel 0
voltage = VoltageInput()
voltage.setDeviceSerialNumber(serial)
voltage.setHubPort(port)
voltage.setChannel(0)
voltage.openWaitForAttachment(5000)

print(f"TMP1101 detected")
print(f"  Serial: {serial}")
print(f"  VINT port: {port}")
print(f"  Thermocouple: Type K")
print()
print("Temperature       Raw voltage")
print("-----------       -----------")

try:
    while True:
        try:
            t = temp.getTemperature()
            v = voltage.getVoltage()
            print(f"{t:8.2f} °C       {v:8.6f} V")
        except Exception:
            pass

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nStopped.")

finally:
    voltage.close()
    temp.close()
