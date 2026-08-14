#!/usr/bin/env python3

from Phidget22.Devices.Manager import Manager
import time


devices = {}
hubs = {}


def on_attach(manager, channel):
    try:
        device_class = channel.getDeviceClassName()
        sku = channel.getDeviceSKU()
        serial = channel.getDeviceSerialNumber()
        hub_port = channel.getHubPort()
        channel_num = channel.getChannel()
        channel_class = channel.getChannelClassName()
        device_name = channel.getDeviceName()

        # Record the actual hub
        if device_class == "PhidgetHub":
            hubs[serial] = {
                "name": device_name,
                "sku": sku,
                "serial": serial,
            }
            return

        # Ignore the generic capabilities exposed by empty VINT ports.
        if sku in {
            "DIGITALINPUT_PORT",
            "DIGITALOUTPUT_PORT",
            "VOLTAGEINPUT_PORT",
            "VOLTAGERATIOINPUT_PORT",
        }:
            return

        # Group physical VINT devices by hub + port + SKU.
        key = (serial, hub_port, sku)

        if key not in devices:
            devices[key] = {
                "name": device_name,
                "sku": sku,
                "serial": serial,
                "hub_port": hub_port,
                "channels": {},
            }

        # Group channels by channel class.
        devices[key]["channels"].setdefault(channel_class, [])
        devices[key]["channels"][channel_class].append(channel_num)

    except Exception as e:
        print(f"Error processing device: {e}")


def print_tree():
    print()
    print("Phidget Hardware")
    print("================")

    if not hubs:
        print("No Phidget hubs found.")
        return

    for serial, hub in sorted(hubs.items()):

        print(f"└── {hub['name']}")
        print(f"    ├── SKU: {hub['sku']}")
        print(f"    └── Serial: {serial}")

        # Devices grouped by hub port
        port_devices = {}

        for device in devices.values():
            if device["serial"] == serial:
                port_devices.setdefault(device["hub_port"], []).append(device)

        if not port_devices:
            continue

        ports = sorted(port_devices)

        for port_index, port in enumerate(ports):

            last_port = port_index == len(ports) - 1
            port_branch = "└──" if last_port else "├──"
            child_indent = "    " if last_port else "│   "

            print(f"    {port_branch} Port {port}")

            port_list = port_devices[port]

            for device_index, device in enumerate(port_list):

                last_device = device_index == len(port_list) - 1
                device_branch = "└──" if last_device else "├──"
                channel_indent = child_indent + ("    " if last_device else "│   ")

                print(
                    f"    {child_indent}{device_branch} "
                    f"{device['name']} ({device['sku']})"
                )

                channel_classes = sorted(device["channels"])

                for class_index, channel_class in enumerate(channel_classes):

                    last_class = class_index == len(channel_classes) - 1
                    class_branch = "└──" if last_class else "├──"
                    channel_child_indent = channel_indent + (
                        "    " if last_class else "│   "
                    )

                    channels = sorted(device["channels"][channel_class])

                    print(
                        f"    {channel_indent}{class_branch} "
                        f"{channel_class}"
                    )

                    for channel_index, channel_num in enumerate(channels):

                        last_channel = channel_index == len(channels) - 1
                        channel_branch = "└──" if last_channel else "├──"

                        print(
                            f"    {channel_child_indent}{channel_branch} "
                            f"Channel {channel_num}"
                        )


manager = Manager()

manager.setOnAttachHandler(on_attach)

manager.open()

print("Scanning for Phidgets...")
time.sleep(2)

manager.close()

print_tree()
