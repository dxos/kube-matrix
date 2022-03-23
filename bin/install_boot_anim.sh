#!/bin/bash

# Install the boot service.

SERVICE_FILE="etc/systemd/system/boot_flash_leds.service"
SCRIPTS_PATH=$(realpath ./scripts)

sudo cat ./$SERVICE_FILE | sed -e 's@__SCRIPTS_PATH__@'$(SCRIPTS_PATH)'@' > /$SERVICE_FILE
sudo systemctl enable boot_flash_leds
