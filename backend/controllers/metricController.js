import Metric from '../models/Metrics.js'; // Ensure the correct path with .js extension

export const addMetric = async (req, res) => {
  try {
    const metric = await Metric.create(req.body);
    res.status(201).json(metric);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

export const getMetrics = async (req, res) => {
  try {
    const metrics = await Metric.findAll({ where: { userId: req.user.id } });
    res.json(metrics);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
