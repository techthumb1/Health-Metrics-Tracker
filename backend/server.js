// server.js

import express from 'express';
import cors from 'cors';
import sequelize from './config/database.js';
import User from './models/User.js'; // Import User model

// Create an Express app
const app = express();
const PORT = process.env.PORT || 5001;

// Middleware
app.use(cors({
  origin: 'http://localhost:3000', // Allow requests from your frontend's domain
  methods: ['GET', 'POST'],       // Allow specific HTTP methods
  allowedHeaders: ['Content-Type'], // Allow specific headers
}));
// Enable CORS for frontend
app.use(express.json()); // Parse JSON request bodies
app.options('/api/metrics', cors()); // Handle CORS preflight for this route

// In-memory store for metrics
let metrics = [];

// Health check route
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

// POST /api/metrics - Log health metrics
app.post('/api/metrics', (req, res) => {
  console.log('Received request body:', req.body);
  const { heartRate, weight, systolic, diastolic } = req.body;

  // Validation: Ensure all fields are present
  if (!heartRate || !weight || !systolic || !diastolic) {
    return res.status(400).json({ error: 'All fields are required' });
  }

  // Create new metric object
  const newMetric = {
    id: metrics.length + 1,
    heartRate: parseInt(heartRate, 10),
    weight: parseFloat(weight),
    systolic: parseInt(systolic, 10),
    diastolic: parseInt(diastolic, 10),
    dateLogged: new Date().toISOString(),
  };

  metrics.push(newMetric); // Save metric in memory
  res.status(201).json({ message: 'Metrics logged successfully', metric: newMetric });
});

// GET /api/metrics - Retrieve all health metrics
app.get('/api/metrics', (req, res) => {
  res.status(200).json({ metrics });
});

// Test + Sync Database
sequelize.authenticate()
  .then(() => console.log('Database connected successfully'))
  .catch(err => console.error('Database connection error:', err));

sequelize.sync({ alter: true })
  .then(() => {
    console.log('Database synchronized successfully');
  })
  .catch(err => {
    console.error('Database synchronization failed:', err);
  });

// Just to see if the User model was imported properly
console.log('User model:', User);

// Start listening
app.listen(PORT, () => {
  console.log(`Node backend listening on port ${PORT}`);
});
