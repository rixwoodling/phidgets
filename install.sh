#!/usr/bin/env bash

set -e

RULE_FILE="/etc/udev/rules.d/99-libphidget22.rules"

echo "Installing Phidgets udev rules..."

sudo tee "$RULE_FILE" > /dev/null <<'EOF'
# All current and future Phidgets
SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="06c2", ATTRS{idProduct}=="00[3-a][0-f]", MODE="666"
EOF

echo "Reloading udev rules..."

sudo udevadm control --reload-rules
sudo udevadm trigger

echo "Phidgets udev rules installed."
echo "Unplug and reconnect the Phidget device."
