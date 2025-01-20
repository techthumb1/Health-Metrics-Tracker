import { Sequelize } from 'sequelize';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

// Set the database name manually if `DB_NAME` is not defined
const DB_NAME = process.env.DB_NAME || 'health_metrics_db';
const DB_USER = process.env.DB_USER || 'jasonrobinson';
const DB_PASSWORD = process.env.DB_PASSWORD || 'your_default_password';
const DB_HOST = process.env.DB_HOST || 'localhost';
const DB_PORT = process.env.DB_PORT || 5432;

console.log('DB_NAME:', DB_NAME); // This should log 'health_metrics_db'

// Initialize Sequelize
const sequelize = new Sequelize(DB_NAME, DB_USER, DB_PASSWORD, {
  host: DB_HOST,
  port: DB_PORT,
  dialect: 'postgres',
  logging: false, // Disable logging for production; enable for debugging if needed
});

// Test the connection
sequelize
  .authenticate()
  .then(() => console.log('Database connection established successfully'))
  .catch((err) => {
    console.error('Unable to connect to the database:', err.message);
    process.exit(1); // Exit the application if the database connection fails
  });

export default sequelize;
