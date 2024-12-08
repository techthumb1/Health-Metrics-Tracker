import sequelize from './config/database.js'; // Import Sequelize instance
import User from './models/User.js'; // Import User model

sequelize.authenticate() // Optional for testing connection
  .then(() => console.log('Database connected successfully'))
  .catch(err => console.error('Database connection error:', err));

sequelize.sync({ alter: true }) // Synchronize database
  .then(() => {
    console.log('Database synchronized successfully');
  })
  .catch(err => {
    console.error('Database synchronization failed:', err);
  });

  console.log('User model:', User);
