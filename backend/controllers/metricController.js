const Metric = require('../models/Metric');

exports.addMetric = async (req, res) => {
  try {
    const metric = await Metric.create({ ...req.body, userId: req.user.id });
    res.status(201).json({ metric });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getMetrics = async (req, res) => {
  try {
    const metrics = await Metric.findAll({ where: { userId: req.user.id } });
    res.json({ metrics });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
