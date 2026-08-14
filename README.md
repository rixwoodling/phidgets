# Phidgets TMP1101 Tools

Basic Python utilities for a **Phidgets HUB0002 VINT Hub** with a **TMP1101 4x Thermocouple Phidget**.

#### `install.sh`
```
git clone https://github.com/rixwoodling/phidgets.git # or unzip download
cd phidgets
python3 -m venv venv
source venv/bin/activate
pip install phidget22
./install.sh
```

## Hardware Scripts

#### `detect_hub.py`
Verifies basic communication with a connected Phidgets VINT Hub. The test automatically discovers the hub, connects to VINT port 0, and reports its device information.
```
python detect_hub.py

Attached!
Device: Hub Port - Digital Input Mode
Device class: PhidgetVINT
SKU: DIGITALINPUT_PORT
Serial: 786276
Hub port: 0
Channel: 0
```

#### `detect_sensor.py`

Scans attached Phidget channels and reports device information discovered by Phidget22.

```text
Scanning for Phidgets...

ATTACHED
  Device:       4x Thermocouple Phidget
  Device class: PhidgetVINT
  Device ID:    89
  SKU:          TMP1101
  Serial:       786276
  Hub port:     0
  Channel:      0
  Channel class:PhidgetTemperatureSensor
...
```
It also reports generic hub port modes. These are **port capabilities**, not necessarily physical devices.

#### `detect_sensor_matrix.py`

Renders the Phidget Manager results as a matrix while retaining device, SKU, serial, port, channel, and channel-class information.
```text
python detect_sensor_matrix.py

┌──────┬────────────────────────────────┬──────────────┬───────────┬────────────┬────────┬─────────┬──────────────────────────┐
│ Port │ Device                         │ Device Class │ Device ID │ SKU        │ Serial │ Channel │ Channel Class            │
├──────┼────────────────────────────────┼──────────────┼───────────┼────────────┼────────┼─────────┼──────────────────────────┤
│ 0    │ 6-Port USB VINT Hub Phidget    │ PhidgetHub   │ 147       │ HUB0002    │ 786276 │ 0       │ PhidgetHub               │
├──────┼────────────────────────────────┼──────────────┼───────────┼────────────┼────────┼─────────┼──────────────────────────┤
│ 0    │ 4x Thermocouple Phidget        │ PhidgetVINT  │ 89        │ TMP1101    │ 786276 │ 0       │ PhidgetTemperatureSensor │
├──────┼────────────────────────────────┼──────────────┼───────────┼────────────┼────────┼─────────┼──────────────────────────┤
│ 0    │ 4x Thermocouple Phidget        │ PhidgetVINT  │ 89        │ TMP1101    │ 786276 │ 1       │ PhidgetTemperatureSensor │
├──────┼────────────────────────────────┼──────────────┼───────────┼────────────┼────────┼─────────┼──────────────────────────┤
...
```

#### `hardware_tree.py`

Displays the connected Phidgets hardware topology as a tree. Automatically discovers the VINT hub, attached devices, available channels, and channel types.
```
python hardware_tree.py

Phidget Hardware
================
└── 6-Port USB VINT Hub Phidget
    ├── SKU: HUB0002
    └── Serial: 786276
    └── Port 0
        └── 4x Thermocouple Phidget (TMP1101)
            ├── PhidgetTemperatureSensor
            │   ├── Channel 0
            │   ├── Channel 1
            │   ├── Channel 2
            │   ├── Channel 3
            │   └── Channel 4
            └── PhidgetVoltageInput
                ├── Channel 0
                ├── Channel 1
                ├── Channel 2
                └── Channel 3
```

## Validation Scripts

#### `tmp1101_monitor0.py`

Reads **Type K thermocouple channel 0** and its corresponding raw voltage input. The TMP1101 and VINT port are discovered automatically.
```text
python tmp1101_monitor0.py

TMP1101 detected
  Serial: 786276
  VINT port: 0
  Thermocouple: Type K

Temperature       Raw voltage
-----------       -----------
   29.05 °C       0.000289 V
   28.63 °C       0.000269 V
   28.42 °C       0.000263 V
   27.78 °C       0.000234 V
   27.44 °C       0.000221 V
   27.14 °C       0.000209 V
   27.01 °C       0.000207 V
   27.63 °C       0.000229 V
   29.87 °C       0.000322 V
```

#### `ambient_temp.py`

Reads the TMP1101's **internal temperature sensor (channel 4)**. This measures the TMP1101 itself, not the external thermocouple.
```text
python ambient_temp.py

Ambient temperature sensor attached!
Device:   4x Thermocouple Phidget
SKU:      TMP1101
Serial:   786276
Hub port: 0
Channel:  4

Ambient temperature:
Ctrl-C to exit
Temperature: 26.82 °C
Temperature: 26.83 °C
Temperature: 26.84 °C
```

### Requirements

```bash
python3 -m pip install phidget22
```

Linux also needs the Phidget22 native library and udev rules so the device can be accessed without `sudo`.

## Hardware
```text
USB
└── HUB0002 6-Port USB VINT Hub
    └── Port 0
        └── TMP1101 4x Thermocouple Phidget
            ├── TemperatureSensor channels 0-3
            ├── TemperatureSensor channel 4 (internal)
            └── VoltageInput channels 0-3
```

### Notes
- External probe: **Type K**.
- Thermocouple polarity matters. Reversed wires invert the temperature response.
- A thermocouple directly exposed to a heater can read much hotter than the surrounding air because the junction absorbs radiant heat.
