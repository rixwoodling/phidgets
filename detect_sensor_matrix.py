#!/usr/bin/env python3

import time
from Phidget22.Devices.Manager import Manager


rows = []


def on_attach(manager, channel):
    try:
        rows.append({
            "device": channel.getDeviceName(),
            "device_class": channel.getDeviceClassName(),
            "device_id": channel.getDeviceID(),
            "sku": channel.getDeviceSKU(),
            "serial": channel.getDeviceSerialNumber(),
            "hub_port": channel.getHubPort(),
            "channel": channel.getChannel(),
            "channel_class": channel.getChannelClassName(),
        })
    except Exception as e:
        print(f"Error processing Phidget: {e}")


def print_matrix():
    if not rows:
        print("No Phidgets detected.")
        return

    # Remove exact duplicate reports while preserving all distinct information.
    unique_rows = []
    seen = set()

    for row in rows:
        key = tuple(row.values())
        if key not in seen:
            seen.add(key)
            unique_rows.append(row)

    # Put the physical hub first, then VINT devices/capabilities by port.
    unique_rows.sort(
        key=lambda r: (
            0 if r["device_class"] == "PhidgetHub" else 1,
            r["hub_port"],
            r["device_id"],
            r["sku"],
            r["channel_class"],
            r["channel"],
        )
    )

    headers = [
        "Port",
        "Device",
        "Device Class",
        "Device ID",
        "SKU",
        "Serial",
        "Channel",
        "Channel Class",
    ]

    data = [
        [
            str(row["hub_port"]),
            row["device"],
            row["device_class"],
            str(row["device_id"]),
            row["sku"],
            str(row["serial"]),
            str(row["channel"]),
            row["channel_class"],
        ]
        for row in unique_rows
    ]

    widths = [
        max(len(headers[i]), *(len(row[i]) for row in data))
        for i in range(len(headers))
    ]

    def line(left, middle, right, fill="─"):
        return (
            left
            + middle.join(fill * (width + 2) for width in widths)
            + right
        )

    def row_line(values):
        return (
            "│ "
            + " │ ".join(
                values[i].ljust(widths[i])
                for i in range(len(headers))
            )
            + " │"
        )

    print()
    print("Phidget Detection Matrix")
    print("=========================")
    print()

    print(line("┌", "┬", "┐"))
    print(row_line(headers))
    print(line("├", "┼", "┤"))

    for index, row in enumerate(data):
        print(row_line(row))
        if index != len(data) - 1:
            print(line("├", "┼", "┤"))

    print(line("└", "┴", "┘"))
    print()
    print(f"Detected entries: {len(data)}")


manager = Manager()
manager.setOnAttachHandler(on_attach)

manager.open()

print("Scanning for Phidgets...")
time.sleep(2)

manager.close()

print_matrix()
