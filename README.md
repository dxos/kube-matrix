# KUBE Matrix

Matrix is a display and device driver for the KUBE device.

<img width="512" alt="Screen Shot 2022-03-23 at 2 02 41 PM" src="https://user-images.githubusercontent.com/3523355/159766169-ce14473c-6910-41e1-a955-c6c9723eeec6.png">

This package consists of the following components:

| Component                | Purpose                                                                            |
|--------------------------|------------------------------------------------------------------------------------|
| `./src/client/web`       | A Web app that generates an animated bitmap that is streamed to the relay server.  |
| `./src/server/express`   | Express server serves the Generator app and API endpoint.                          |
| `./src/server/relay`     | Relays the Generator bitmap via Websocket to Python server via MQTT.               |
| `./src/client/generator` | Web app that streams bitmaps to the Express server.                                |
| `./scripts/server`       | Python server that controls the LED array via bitmaps streamed to its MQTT.        |

Additionally there are multiple scripts (see `./scripts`) that can be used to control the Matrix display.


## Setup

The system assumes that `node` and `python3` are installed.

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

Create the Web server's TLS (https) credentials.

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt
```

Install the boot service to trigger the animation on startup:

```bash
sudo ./bin/install_boot_anim.sh
```

## Development

Start the app server in development mode.

```bash
yarn dev
```

To test the server.

```bash
curl -s http://localhost:8000/info | jq
```

To POST to the API endpoint:

```bash
curl -s -X POST localhost:8000/api -H "Content-Type: application/json" -d '{ "action": "test" }' | jq
```

## Running

```bash
node ./src/express.js
node ./src/relay.js
sudo python3 ./scripts/server.py
```

To bypass Chrome's unsafe Cert warning, type `thisisunsafe` when loading the app via `https`.
