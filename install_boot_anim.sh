#!/bin/bash

sudo ln -s /home/ubuntu/kube-field/etc/systemd/system/boot_flash_leds.service /etc/systemd/system/boot_flash_leds.service
sudo systemctl enable boot_flash_leds
