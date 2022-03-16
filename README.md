# KUBE Field

A web app to control the LED array on the 10X KUBE hardware prototype. 
A Python program controls the LEDs and receives frames of LED animation over MQTT. 
A Node.js server hosts the web application which generates the animations on the client side
and streams the frames back over a WebSocket. 
The server then sends the frames over MQTT to the Python program.

## Setup

```bash
cd ./scripts

# Install dependencies
sudo apt install python3-pip mosquitto
python3 -m pip install -r requirements.txt
yarn

# Create the certificates for the HTTPS server
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt
```

### Flash on Boot

There is a simple animation in `boot_anim.py` that is invoked by a systemd service file in `/etc/systemd/system`. 
The `install_boot_anim.sh` script can be used to install and enable the systemd service. 
This repo must be installed in `/home/ubuntu/kube-field` for the animation to run.

## Running

```bash
sudo python3 ./scripts/leds.py
node ./src/server/server.js
```

To bypass Chrome's unsafe Cert warning, type `thisisunsafe` with the main screen focused.


## Integration

Take a look at `led_demo_simple.py` for a minimal example of writing to the LED array.

