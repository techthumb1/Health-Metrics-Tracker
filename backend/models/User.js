import { DataTypes } from 'sequelize';
import sequelize from '../config/database.js'; // Ensure .js extension for ES modules

const User = sequelize.define('User', {
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
  },
  password: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  isPremium: {
    type: DataTypes.BOOLEAN,
    defaultValue: false,
  },
});

export default User;

console.log('User model initialized:', User);
