from pymongo import MongoClient
import bson
from dotenv import load_dotenv
import os

class GridFSChunkHandler:
    def __init__(self, host='localhost', port=27017, db_name='admin'):
        load_dotenv()
        username = os.getenv("BD_USERNAME")
        password = os.getenv("DB_PASSWORD")
        db = os.getenv("DB_NAME")
        connection_str = f"mongodb://{username}:{password}@{host}:{port}/{db_name}"
        self.client = MongoClient(connection_str)
        self.db = self.client[db]
        self.fs_files = self.db['fs.files']
        self.fs_chunks = self.db['fs.chunks']

    def insert_chunk(self, file_id, chunk_number, data):
        chunk_data = {
            'files_id': file_id,
            'n': chunk_number,
            'data': bson.Binary(data)
        }
        result = self.fs_chunks.insert_one(chunk_data)
        return result.inserted_id

    def insert_file_metadata(self, file_id, filename, file_size, chunk_size):
        file_data = {
            '_id': file_id,
            'filename': filename,
            'length': file_size,
            'chunkSize': chunk_size,
            'uploadDate': bson.datetime.datetime.utcnow()
            # Agrega más campos según tus necesidades
        }
        result = self.fs_files.insert_one(file_data)
        return result.inserted_id

# Uso de la clase
#handler = GridFSChunkHandler()
#chunk_size = 255 * 1024  # tamaño del chunk
#file_id = bson.ObjectId()  # Crear un nuevo ObjectId para este archivo

#with open('testfile.txt', 'rb') as f:
#    file_size = 0
#    chunk_number = 0
#    while True:
#        chunk = f.read(chunk_size)
#        if not chunk:
#            break
#        
#        handler.insert_chunk(file_id, chunk_number, chunk)
#        chunk_number += 1
#        file_size += len(chunk)
#
#    handler.insert_file_metadata(file_id, 'testfile.txt', file_size, chunk_size)
#