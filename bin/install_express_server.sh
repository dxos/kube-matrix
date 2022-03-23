#!/bin/bash

# Install the LED express server.

SERVICE_FILE="etc/systemd/system/express_flash_leds.service"
SRC_PATH=$(realpath ./src)

sudo cat ./$SERVICE_FILE | sed -e 's@__SRC_PATH__@'$SRC_PATH'@' > /$SERVICE_FILE
sudo systemctl enable express_flash_leds
