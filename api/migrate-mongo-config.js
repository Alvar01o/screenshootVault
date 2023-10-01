require('dotenv').config();

const config = {
    mongodb: {
      url: process.env.MONGO_URI,
      databaseName: 'vault',
      options: {
        useNewUrlParser: true,
        useUnifiedTopology: true,
      },
    },
    migrationsDir: 'migrations',
    changelogCollectionName: 'changelog',
  };
  
  module.exports = config;