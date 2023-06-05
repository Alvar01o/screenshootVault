import socket
import struct
import os
import pickle
from io import BytesIO
from PIL import Image
import sys

# Obtener el directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta del directorio superior
parent_dir = os.path.dirname(current_dir)
# Agregar la ruta del directorio superior a sys.path
sys.path.append(parent_dir)
from vault_codes.utilFunctions import calculate_buffer_size, custom_progress_bar
from vault_codes.customClasses import TransferInfo
class UDPServer:
    
    def __init__(self, ip, port, image_dir, logger, transferInfo):
        self.ip = ip
        self.logger = logger
        self.port = port
        self.info = transferInfo
        self.image_dir = image_dir

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

    def receive_image(self):
        self.logger.info(f"Ready to receive in port {self.port}")
        # Crear un socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 64 * 1024)
        sock.bind((self.ip, self.port))
        self.info.status = TransferInfo.BUSY
        file_info, _ = sock.recvfrom(4096)
        file_name, received_hash_sha1 = file_info.decode('utf-8').split('|')
        self.logger.info(f"Filename, UserHash: {file_name}, {received_hash_sha1}")
        # Recibir el tamaño de la imagen como un entero (4 bytes)
        data, _ = sock.recvfrom(4)
        self.img_len = struct.unpack('<L', data)[0]
        self.info.udpInfo.img_length = self.img_len
        self.logger.info(f"Total image size: {self.img_len} bytes")
        self.buffer_size = calculate_buffer_size(self.img_len)
        self.info.udpInfo.buffer_size = self.buffer_size
        # Recibir la imagen en paquetes de buffer_size bytes
        self.img_bytes = bytearray()
        received_size = 0
        while len(self.img_bytes) < self.img_len:
            # Recibir el tamaño del objeto serializado
            data, _ = sock.recvfrom(4)
            serialized_packet_size = struct.unpack('<L', data)[0]
            # Recibir paquete serializado y deserializarlo
            serialized_packet, _ = sock.recvfrom(serialized_packet_size)
            packet = pickle.loads(serialized_packet)
            
            # Agregar datos de imagen al bytearray
            self.img_bytes.extend(packet.data)
            self.info.udpInfo.packet_status_array.extend(packet.data)
            received_size += len(packet.data)
            progress = received_size / self.img_len
            progress_bar = custom_progress_bar(progress)
            self.logger.info(f"Progress: {progress * 100:.2f}% {progress_bar}")
        # save the file here.. 
        #me quede en recibir los paquetes por orden
        # check if all the data is on self.info.packet_status_array 
        # Cerrar el socket
        self.logger.info('Received Succefully.')
        sock.close()
        # Convertir el array de bytes en una imagen y guardarla
        img = Image.open(BytesIO(self.img_bytes))
        # Guardar la imagen en un archivo
        # Si el directorio no existe, se crea
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
        if not os.path.exists(os.path.join(self.image_dir, received_hash_sha1)):
            os.makedirs(os.path.join(self.image_dir, received_hash_sha1))
        image_final_dir = os.path.join(self.image_dir, received_hash_sha1, file_name)
        self.info.udpInfo.file_name = image_final_dir
        img.save(image_final_dir)
        self.info.status = TransferInfo.AVAILABLE
        #reset thread
#        self.buffer_size = 0
#        self.img_len = 0
#        self.img_bytes = bytearray()
#        self.logger.info(self.info)
        self.receive_image()

