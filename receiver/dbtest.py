import threading
from dotenv import load_dotenv
import os
import sys
import bson
# Obtener el directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta del directorio superior
parent_dir = os.path.dirname(current_dir)

# Agregar la ruta del directorio superior a sys.path
sys.path.append(parent_dir)

from vault_codes.UdpServer import UDPServer
from vault_codes.customClasses import UdpInfo, TransferInfo
from db import GridFSChunkHandler

if __name__ == "__main__":
    # Uso de la clase
    handler = GridFSChunkHandler()
    chunk_size = 255 * 1024  # tamaño del chunk
    file_id = bson.ObjectId()  # Crear un nuevo ObjectId para este archivo

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