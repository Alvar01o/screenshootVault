import socket
import struct
import logging
import os
import threading
import pickle
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import sys
sys.path.append('.')
import utilFunctions



class UDPServer:

    def __init__(self, ip, port, image_dir):
        self.ip = ip
        self.port = port
        self.image_dir = image_dir
        self.buffer_size = 0
        self.img_len = 0
        self.img_bytes = bytearray()

    def receive_image(self):
        global ip, image_dir
        logging.info('Receiving image.')
        # Crear un socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 64 * 1024)
        sock.bind((self.ip, self.port))

        # Recibir el nombre del archivo y el hash SHA1
        file_info, _ = sock.recvfrom(4096)
        file_name, received_hash_sha1 = file_info.decode('utf-8').split('|')

        #received_hash_sha1 = received_hash_sha1.decode('utf-8')
        logging.info(f"user and file: {file_name}, {received_hash_sha1}")

        # Recibir el tamaño de la imagen como un entero (4 bytes)
        data, _ = sock.recvfrom(4)
        self.img_len = struct.unpack('<L', data)[0]

        logging.info(f"Total image size: {self.img_len} bytes")

        self.buffer_size = utilFunctions.calculate_buffer_size(self.img_len)

        # Recibir la imagen en paquetes de buffer_size bytes
        self.img_bytes = bytearray()
        received_size = 0
        while len(self.img_bytes) < self.img_len:
            data, _ = sock.recvfrom(self.buffer_size)
            self.img_bytes += data
            received_size += len(data)
            progress = received_size / self.img_len
            progress_bar = utilFunctions.custom_progress_bar(progress)
            logging.info(f"Progress: {progress * 100:.2f}% {progress_bar}")

        # Cerrar el socket
        logging.info('closing socket.')
        sock.close()
        # Convertir el array de bytes en una imagen y guardarla
        img = Image.open(BytesIO(self.img_bytes))
        # Guardar la imagen en un archivo
        # Si el directorio no existe, se crea
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
        if not os.path.exists(os.path.join(self.image_dir, received_hash_sha1)):
            os.makedirs(os.path.join(self.image_dir, received_hash_sha1))
        img.save(os.path.join(self.image_dir, received_hash_sha1, file_name))

if __name__ == "__main__":
    load_dotenv()
    ip = os.getenv("SERVER_IP")
    min_port = int(os.getenv("MIN_PORT"))
    max_port = int(os.getenv("MAX_PORT"))
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Starting server udp..')
    image_dir = os.getenv("IMAGE_DIR")
    for port in range(min_port, max_port + 1):
        server = UDPServer(ip, port, image_dir)
        logging.info(f'Starting server udp on port: {port}')
        t = threading.Thread(target=server.receive_image)
        t.start()
