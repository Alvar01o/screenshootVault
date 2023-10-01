module.exports = {
    async up(db) {
      await db.createCollection('teams');
    },
  
    async down(db) {
      await db.collection('teams').drop();
    },
  };