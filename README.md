# KUBE Field

A web app to control the LED array on the 10X Kube hardware prototype. A Python
program controls the LEDs and receives frames of LED animation over MQTT. A Node.js
server hosts the web application which generates the animations on the client side
and streams the frames back over a WebSocket. The server then sends the frames over
MQTT to the Python program.

## Setup

```
# Install dependencies
sudo apt install mosquitto paho-mqtt
python3 -m pip install -r requirements.txt

# Create the certificates for the HTTPS server
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt
```

## Running

```
sudo python3 leds.py
node server.js
```
