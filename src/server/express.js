//
// Web server.
//

// TODO(burdon): Conver to Typescript.

const cors = require('cors');
const fs = require('fs');
const http = require('http');
const https = require('https');
const express = require('express');

const { name, version } = require('../../package.json');
const apiService = require('./api');

const HTTP_PORT = 8000;
const HTTPS_PORT = 8001;

// Generated with:
// openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt
const options = {
  key: fs.readFileSync('./credentials/server.key'),
  cert: fs.readFileSync('./credentials/server.crt'),
};

const app = express();

// Enable access for apps served from different domain.
// https://expressjs.com/en/resources/middleware/cors.html
app.use(cors());

// Generator app.
app.use(express.static('public'));
app.use('/js', express.static('src/client'));

// Status API.
app.use(express.json());
app.get('/info', (req, res) => res.send(JSON.stringify({ name, version })));
app.post('/api', async (req, res) => res.json(await apiService(req.body)));

// Start server.
// app.listen(8000);
http.createServer(app).listen(HTTP_PORT, () => console.log(`Started: http://localhost:${HTTP_PORT}`));
https.createServer(options, app).listen(HTTPS_PORT, () => console.log(`Started: https://localhost:${HTTPS_PORT}`));
