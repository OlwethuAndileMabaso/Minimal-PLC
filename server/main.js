'use strict';

const express = require('express');
const http = require('http');
const path = require('path');
const bodyParser = require('body-parser');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);

// --- Configuration ---
const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || '0.0.0.0';
const CLIENT_BUILD = path.join(__dirname, '../client/dist/minimal-plc-client/browser');

// --- Rate limiting ---
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 500,
  standardHeaders: true,
  legacyHeaders: false
});

// --- Middleware ---
app.use(limiter);
app.use(morgan('combined'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// CORS for dev
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  if (req.method === 'OPTIONS') return res.sendStatus(200);
  next();
});

// --- Socket.io ---
const io = new Server(server, {
  cors: { origin: '*', methods: ['GET', 'POST'] }
});

io.on('connection', (socket) => {
  console.log(`[Socket.io] Client connected: ${socket.id}`);

  // Emit simulated tag values every second
  const tagInterval = setInterval(() => {
    socket.emit('tags', {
      timestamp: new Date().toISOString(),
      values: {
        'Zone3Temp': (25 + Math.random() * 10).toFixed(1),
        'SupplyAirTemp': (18 + Math.random() * 5).toFixed(1),
        'FanSpeed': Math.floor(1200 + Math.random() * 400)
      }
    });
  }, 1000);

  socket.on('disconnect', () => {
    clearInterval(tagInterval);
    console.log(`[Socket.io] Client disconnected: ${socket.id}`);
  });
});

// --- REST API Routes ---

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', version: '1.0.0', uptime: process.uptime() });
});

// Devices (mock)
app.get('/api/devices', (req, res) => {
  res.json([
    { id: 1, name: 'EasyIO FT-04', protocol: 'BACnet/IP', ip: '192.168.1.50', tags: 12, online: true },
    { id: 2, name: 'EasyIO FW-14', protocol: 'BACnet/IP', ip: '192.168.1.51', tags: 8, online: true },
    { id: 3, name: 'OpenPLC Runtime', protocol: 'Modbus TCP', ip: '192.168.1.10', tags: 24, online: false }
  ]);
});

// Alarms (mock)
app.get('/api/alarms', (req, res) => {
  res.json([
    { id: 1, severity: 'critical', message: 'Zone 3 Temp > 30°C', time: '14:32', acknowledged: false },
    { id: 2, severity: 'warning', message: 'Supply Air < 15°C', time: '13:15', acknowledged: false },
    { id: 3, severity: 'critical', message: 'Chiller Fault', time: '12:01', acknowledged: false },
    { id: 4, severity: 'normal', message: 'Fan 1 restored', time: '11:45', acknowledged: true }
  ]);
});

// Tags (mock)
app.get('/api/tags', (req, res) => {
  res.json([
    { id: 1, name: 'Zone3Temp', value: 28.5, unit: '°C', deviceId: 1 },
    { id: 2, name: 'SupplyAirTemp', value: 19.2, unit: '°C', deviceId: 1 },
    { id: 3, name: 'FanSpeed', value: 1450, unit: 'RPM', deviceId: 3 }
  ]);
});

// --- Serve Angular build in production ---
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(CLIENT_BUILD));
  app.get('*', (req, res) => {
    res.sendFile(path.join(CLIENT_BUILD, 'index.html'));
  });
}

// --- Start server ---
server.listen(PORT, HOST, () => {
  console.log(`\n  ⚡ Minimal-PLC Server`);
  console.log(`  ─────────────────────`);
  console.log(`  HTTP  : http://${HOST === '0.0.0.0' ? 'localhost' : HOST}:${PORT}`);
  console.log(`  API   : http://localhost:${PORT}/api`);
  console.log(`  Health: http://localhost:${PORT}/api/health\n`);
});

module.exports = { app, server };
