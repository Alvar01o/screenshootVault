import socket
import struct
import os
import pickle
import select

from io import BytesIO
from PIL import Image
import sys
import bson
# Obtener el directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta del directorio superior
parent_dir = os.path.dirname(current_dir)
# Agregar la ruta del directorio superior a sys.path
sys.path.append(parent_dir)
from vault_codes.utilFunctions import calculate_buffer_size, custom_progress_bar
from vault_codes.customClasses import TransferInfo
from db import GridFSChunkHandler
class UDPServer:
    
    def __init__(self, ip, port, image_dir, logger, transferInfo):
        self.ip = ip
        self.logger = logger
        self.port = port
        self.info = transferInfo
        self.image_dir = image_dir
        self._running = True
        self.sock = None
        self._select_time_out = 10

    @property
    def buffer_size(self):
        return self._buffer_size
    
    @buffer_size.setter
    def buffer_size(self, valor):
        self.info.udpInfo.buffer_size = valor
        self._buffer_size = valor

    @property
    def img_len(self):
        return self._img_len
    
    @img_len.setter
    def img_len(self, valor):
        self.info.udpInfo.img_length = valor
        self._img_len = valor

    @property
    def image_dir(self):
        return self._image_dir
    
    @image_dir.setter
    def image_dir(self, valor):
        self.info.udpInfo.file_name = valor
        self._image_dir = valor

    def set_logging(self, logger):
        self.logger = logger

    def stop(self):
        self._running = False
        self.sock.close()  #
        
    def show_progress(self, received, total):
        progress = received  / total
        progress_bar = custom_progress_bar(progress)
        self.logger.info(f"Progress: {progress * 100:.2f}% {progress_bar}")
    
    def receive_image(self):
        try :
            # Crear un socket UDP
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 64 * 1024)
            self.sock.bind((self.ip, self.port))
            self.info.status = TransferInfo.BUSY
            ready = select.select([self.sock], [], [], self._select_time_out)
            gridfs_handler = GridFSChunkHandler()
            if ready[0]:
                file_info, _ = self.sock.recvfrom(4096)
                file_name, received_hash_sha1 = file_info.decode('utf-8').split('|')
                self.logger.info(f"Filename, UserHash: {file_name}, {received_hash_sha1}")
                # Recibir el tamaño de la imagen como un entero (4 bytes)
                data, _ = self.sock.recvfrom(4)
                self.img_len = struct.unpack('<L', data)[0]

                self.logger.info(f"Total image size: {self.img_len} bytes")
                self.buffer_size = calculate_buffer_size(self.img_len)
                # Recibir la imagen en paquetes de buffer_size bytes
                self.img_bytes = bytearray()
                chunk_number = 0
                file_id = bson.ObjectId()
                while len(self.img_bytes) < self.img_len:
                    # Recibir el tamaño del objeto serializado
                    data, _ = self.sock.recvfrom(4)
                    serialized_packet_size = struct.unpack('<L', data)[0]
                    # Recibir paquete serializado y deserializarlo
                    serialized_packet, _ = self.sock.recvfrom(serialized_packet_size)
                    packet = pickle.loads(serialized_packet)
                    gridfs_handler.insert_chunk(file_id, chunk_number, packet.data);
                    # Agregar datos de imagen al bytearray
                    self.img_bytes.extend(packet.data)
                    chunk_number += 1 
                    self.info.udpInfo.add_custom_package(packet.identifier, packet.data)
                    self.show_progress(self.info.udpInfo.get_bytes_received(), self.img_len)
                self.sock.close()
                # Convertir el array de bytes en una imagen y guardarla
                img = Image.open(BytesIO(self.img_bytes))
                # Guardar la imagen en un archivo
                # Si el directorio no existe, se crea
                if not os.path.exists(self.image_dir):
                    os.makedirs(self.image_dir)
                if not os.path.exists(os.path.join(self.image_dir, received_hash_sha1)):
                    os.makedirs(os.path.join(self.image_dir, received_hash_sha1))
                image_final_dir = os.path.join(self.image_dir, received_hash_sha1, file_name)
                gridfs_handler.insert_file_metadata(file_id, file_name, self.img_len,  self.buffer_size)
                self.info.udpInfo.file_name = image_final_dir
                img.save(image_final_dir)
                self.info.status = TransferInfo.AVAILABLE
                self.receive_image()
            else:
                self.sock.close()
                if self._running:
                    self.receive_image()
        except Exception as e:
            print('closing Threat')
            print(str(e))
            self.stop()

