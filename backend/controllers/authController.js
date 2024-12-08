import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import User from '../models/User.js'; // Ensure the correct path with .js extension

export const register = async (req, res) => {
  try {
    console.log('Register endpoint called with data:', req.body); // Debug log
    const { email, password } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);
    const user = await User.create({ email, password: hashedPassword });
    res.status(201).json({ user });
  } catch (error) {
    console.error('Register Error:', error.message);
    res.status(500).json({ error: error.message });
  }
};


export const login = async (req, res) => {
  try {
    const { email, password } = req.body;
    const user = await User.findOne({ where: { email } });
    if (!user || !(await bcrypt.compare(password, user.password))) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    const token = jwt.sign(
      { id: user.id, email: user.email },
      process.env.JWT_SECRET,
      { expiresIn: '1h' } // Optional: Token expiration time
    );
    res.json({ token });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};import Metric from '../models/Metrics.js'; // Ensure the correct path with .js extension

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
