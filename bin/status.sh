#!/bin/bash

# Run as root.

systemctl status kube_matrix_boot.service
systemctl status kube_matrix_server.service

curl -s http://localhost:8000/info | jq

curl -s -X POST localhost:8000/api -H "Content-Type: application/json" -d '{ "action": "test" }' | jq
