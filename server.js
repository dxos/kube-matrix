const fs = require('fs');
const https = require('https');
const express = require('express');
const WebSocket = require('ws');
const mqtt = require('mqtt');
//const { createCanvas } = require('canvas');

const PORT = 8000;

const client = mqtt.connect('mqtt://127.0.0.1');
//const canvas = createCanvas(11, 11);
//const ctx = canvas.getContext('2d');

// Generated with:
//  openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt
const options = {
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.crt'),
};

const app = express();
app.use(express.static('public'));

const server = https.createServer(options, app);
server.listen(PORT, () => console.log(`https://localhost:${PORT}`));

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

