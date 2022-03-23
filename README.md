# KUBE Field

A Web app can be used to select animations which are streamed to the Python server.
Alternatively the individual Python "run" scripts can be invoked via the HTTP API endpoint.

This package consists of the following components:

| Component                | Purpose                                                                     |
|--------------------------|-----------------------------------------------------------------------------|
| `./src/server/express`   | Express server serves the Generator app and API endpoint.                   |
| `./src/server/relay`     | Relays Generator bitmap via Websocket to Python server via MQTT.            |
| `./src/client/generator` | Web app that streams bitmaps to the Express server.                         |
| `./scripts/server`       | Python server that controls the LED array via bitmaps streamed to its MQTT. |

## Setup

Install yarn dependencies.

```bash
yarn 
```

Install Python dpeendencies.

```bash
cd ./scripts
sudo apt install python3-pip mosquitto
python3 -m pip install -r requirements.txt
```

Create the server's TLS (https) credentials.

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt
```

## Development

Start the app server.

```bash
yarn start
```

To test the server.

```bash
curl -s http://localhost:8000/info | jq
```

To POST to the API endpoint:

```bash
curl -s -X POST localhost:8000/api -H "Content-Type: application/json" -d '{ "action": "test" }' | jq
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

