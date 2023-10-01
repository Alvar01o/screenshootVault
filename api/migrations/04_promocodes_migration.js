module.exports = {
    async up(db) {
      await db.createCollection('promocodes');
    },
  
    async down(db) {
      await db.collection('promocodes').drop();
    },
  };