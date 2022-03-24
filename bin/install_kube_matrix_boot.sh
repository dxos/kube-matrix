#!/bin/bash

# Install the boot service.

SERVICE_FILE="etc/systemd/system/kube_matrix_boot.service"
ROOT_PATH=$(realpath .)

sudo cat ./$SERVICE_FILE | sed -e 's@__ROOT__@'$ROOT_PATH'@' > /$SERVICE_FILE
sudo systemctl enable kube_matrix_boot
