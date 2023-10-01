module.exports = {
    async up(db) {
      await db.createCollection('files');
    },
  
    async down(db) {
      await db.collection('files').drop();
    },
  };