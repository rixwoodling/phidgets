#!/usr/bin/env python3

import time
from Phidget22.Phidget import Phidget
from Phidget22.Devices.TemperatureSensor import TemperatureSensor
from Phidget22.Devices.VoltageInput import VoltageInput
from Phidget22.ThermocoupleType import ThermocoupleType


# Temperature color range
MIN_TEMP = 0.0
MAX_TEMP = 100.0


def temperature_color(temp):
    """Return ANSI truecolor escape sequence for a temperature."""

    # Clamp temperature to our color range
    value = max(MIN_TEMP, min(MAX_TEMP, temp))

    # Normalize 0.0 -> 1.0
    ratio = (value - MIN_TEMP) / (MAX_TEMP - MIN_TEMP)

    # Blue -> Cyan -> Green -> Yellow -> Red
    if ratio < 0.25:
        r = 0
        g = int(255 * (ratio / 0.25))
        b = 255

    elif ratio < 0.50:
        r = 0
        g = 255
        b = int(255 * (1 - (ratio - 0.25) / 0.25))

    elif ratio < 0.75:
        r = int(255 * ((ratio - 0.50) / 0.25))
        g = 255
        b = 0

    else:
        r = 255
        g = int(255 * (1 - (ratio - 0.75) / 0.25))
        b = 0

    return f"\033[38;2;{r};{g};{b}m"


RESET = "\033[0m"


# Find the first TemperatureSensor channel on any Phidget
temp = TemperatureSensor()
temp.setDeviceSerialNumber(Phidget.ANY_SERIAL_NUMBER)
temp.setHubPort(Phidget.ANY_HUB_PORT)
temp.setChannel(0)
temp.openWaitForAttachment(5000)

serial = temp.getDeviceSerialNumber()
port = temp.getHubPort()

temp.setThermocoupleType(
    ThermocoupleType.THERMOCOUPLE_TYPE_K
)


# Same physical TMP1101, raw voltage channel 0
voltage = VoltageInput()
voltage.setDeviceSerialNumber(serial)
voltage.setHubPort(port)
voltage.setChannel(0)
voltage.openWaitForAttachment(5000)


print("TMP1101 detected")
print(f"  Serial: {serial}")
print(f"  VINT port: {port}")
print("  Thermocouple: Type K")
print()
print("Temperature       Raw voltage")
print("-----------       -----------")


try:
    while True:
        try:
            t = temp.getTemperature()
            v = voltage.getVoltage()

            color = temperature_color(t)

            print(
                f"{color}{t:8.2f} °C{RESET}"
                f"       {v:8.6f} V"
            )

        except Exception:
            pass

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nStopped.")

finally:
    voltage.close()
    temp.close()
