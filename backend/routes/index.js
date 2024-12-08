import express from 'express';
import { register, login } from '../controllers/authController.js';
import { addMetric, getMetrics } from '../controllers/metricController.js';
import authMiddleware from '../middleware/authMiddleware.js';

const router = express.Router();

// Auth routes
router.post('/register', register);
router.post('/login', login);

// Metric routes
router.post('/metrics', authMiddleware, addMetric);
router.get('/metrics', authMiddleware, getMetrics);

export default router; // Use ES module syntax for export
