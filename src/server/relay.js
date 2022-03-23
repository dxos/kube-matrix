//
// Relay server
// Communicates via MQTT to the Python server.
//

const WebSocket = require('ws');
const mqtt = require('mqtt');

//
// Web relay server.
//

// Python server listens for data stream.
const client = mqtt.connect('mqtt://127.0.0.1');

const wss = new WebSocket.Server({ server });

wss.on('connection', (ws, req) => {
  ws.remoteAddress = req.socket.remoteAddress;
  console.log(`New connection from ${ws.remoteAddress}`);

  ws.on('disconnection', () => {
    console.log(`Lost connection from ${ws.remoteAddress}`);
  });

  ws.on('message', (msg) => {
    const ledUpdate = JSON.parse(msg);
    const data = ledUpdate.reduce((data, row) => data.concat(row.reduce((data, pixel) => data.concat(pixel), [])), []);
    client.publish('dxos', data.join(','));
  });
});
