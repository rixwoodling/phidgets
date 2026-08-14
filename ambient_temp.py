#!/usr/bin/env python3

import time

from Phidget22.Phidget import Phidget
from Phidget22.Devices.TemperatureSensor import TemperatureSensor


sensor = TemperatureSensor()

# Automatically find a TMP1101 on any hub/port.
sensor.setDeviceSerialNumber(Phidget.ANY_SERIAL_NUMBER)
sensor.setHubPort(Phidget.ANY_HUB_PORT)

# TMP1101 channel 4 = internal ambient temperature
sensor.setChannel(4)

try:
    sensor.openWaitForAttachment(5000)

    print("Ambient temperature sensor attached!")
    print(f"Device:   {sensor.getDeviceName()}")
    print(f"SKU:      {sensor.getDeviceSKU()}")
    print(f"Serial:   {sensor.getDeviceSerialNumber()}")
    print(f"Hub port: {sensor.getHubPort()}")
    print(f"Channel:  {sensor.getChannel()}")
    print()
    print("Ambient temperature:")
    print("Ctrl-C to exit")

    while True:
        try:
            temperature = sensor.getTemperature()
            print(f"Temperature: {temperature:.2f} °C")
        except Exception:
            pass

        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    sensor.close()
