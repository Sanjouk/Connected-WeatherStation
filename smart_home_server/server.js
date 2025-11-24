// Install dependencies:
// npm install express mongoose body-parser

const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// --- Middleware ---
app.use(bodyParser.json());



mongoose.connect('mongodb://localhost:27017/Smart_Home');

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));
db.once('open', () => console.log('MongoDB connected'));

// --- Schema ---
const telemetrySchema = new mongoose.Schema({
  timestamp: { type: Date, default: Date.now },
  temperature: Number,
  humidity: Number,
  light: Number,
  motion: Boolean
},{ versionKey: false });

const Telemetry = mongoose.model('Telemetry', telemetrySchema);

// --- Routes ---
app.post('/telemetry', async (req, res) => {
  try {
    const data = new Telemetry({
      temperature: req.body.temperature,
      humidity: req.body.humidity,
      light: req.body.ldr || req.body.light,
      motion: req.body.pir || req.body.motion
    });

    await data.save();
    res.json({ status: 'ok' });
    console.log('Saved telemetry:', data);
  } catch (err) {
    console.error(err);
    res.status(500).json({ status: 'error', message: err.message });
  }
});

// --- Get all telemetry data ---
app.get('/telemetry', async (req, res) => {
  try {
    const data = await Telemetry.find().sort({ timestamp: -1 }); // newest first
    res.json(data);
  } catch (err) {
    console.error(err);
    res.status(500).json({ status: 'error', message: err.message });
  }
});


// --- Start Server ---
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
