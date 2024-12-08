import { DataTypes } from 'sequelize';
import sequelize from '../config/database.js';

const Metric = sequelize.define('Metric', {
  userId: {
    type: DataTypes.INTEGER,
    allowNull: false,
  },
  heartRate: {
    type: DataTypes.FLOAT,
    allowNull: false,
  },
  weight: {
    type: DataTypes.FLOAT,
    allowNull: false,
  },
  systolic: {
    type: DataTypes.FLOAT,
    allowNull: true,
  },
  diastolic: {
    type: DataTypes.FLOAT,
    allowNull: true,
  },
});

export default Metric;
