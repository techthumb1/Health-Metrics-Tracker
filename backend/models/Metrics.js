const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Metric = sequelize.define('Metric', {
  userId: {
    type: DataTypes.INTEGER,
    allowNull: false,
  },
  heartRate: DataTypes.FLOAT,
  systolic: DataTypes.FLOAT,
  diastolic: DataTypes.FLOAT,
  weight: DataTypes.FLOAT,
  rbc: DataTypes.FLOAT,
  wbc: DataTypes.FLOAT,
  hemoglobin: DataTypes.FLOAT,
});

module.exports = Metric;
