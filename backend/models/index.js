import fs from 'fs';
import path from 'path';
import { Sequelize } from 'sequelize';
import process from 'process';
import config from '../config/config.js'; // Use the updated config.js file

const basename = path.basename(import.meta.url);
const env = process.env.NODE_ENV || 'development';
const db = {};

const sequelize = config[env].use_env_variable
  ? new Sequelize(process.env[config[env].use_env_variable], config[env])
  : new Sequelize(
      config[env].database,
      config[env].username,
      config[env].password,
      config[env]
    );

// Dynamically import all model files in the directory
fs.readdirSync(path.resolve())
  .filter(file => {
    return (
      file.indexOf('.') !== 0 &&
      file !== basename &&
      file.slice(-3) === '.js' &&
      file.indexOf('.test.js') === -1
    );
  })
  .forEach(async file => {
    const model = (await import(path.join(path.resolve(), file))).default(
      sequelize,
      Sequelize.DataTypes
    );
    db[model.name] = model;
  });

// Set up model associations if defined
Object.keys(db).forEach(modelName => {
  if (db[modelName].associate) {
    db[modelName].associate(db);
  }
});

db.sequelize = sequelize;
db.Sequelize = Sequelize;

export default db;
