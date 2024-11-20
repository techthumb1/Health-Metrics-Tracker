const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');
const metricController = require('../controllers/metricController');
const authMiddleware = require('../middleware/authMiddleware');

router.post('/register', authController.register);
router.post('/login', authController.login);
router.post('/metrics', authMiddleware, metricController.addMetric);
router.get('/metrics', authMiddleware, metricController.getMetrics);

module.exports = router;
