import socket
import struct
import logging
import os
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import sys
sys.path.append('.')
import utilFunctions

ip = ''
port = ''

def receive_image():
    global ip, port
    logging.info('Receiving image.')
    # Crear un socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 64 * 1024)
    sock.bind((ip, port))

    # Recibir el nombre del archivo como un string
    filename, _ = sock.recvfrom(1024)
    filename = filename.decode('utf-8')

    # Recibir el tamaño de la imagen como un entero (4 bytes)
    data, _ = sock.recvfrom(struct.calcsize('<L'))
    img_len = struct.unpack('<L', data)[0]

    logging.info(f"Total image size: {img_len} bytes")

    # Recibir la imagen en paquetes de tamaño buffer_size
    img_bytes = b""
    received_size = 0
    buffer_size = utilFunctions.calculate_buffer_size(img_len)

    while len(img_bytes) < img_len:
        data, _ = sock.recvfrom(buffer_size)
        img_bytes += data
        received_size += len(data)
        progress = received_size / img_len
        progress_bar = utilFunctions.custom_progress_bar(progress)
        logging.info(f"Progress: {progress * 100:.2f}% {progress_bar}")

    # Cerrar el socket
    logging.info('closing socket.')
    sock.close()
    # Convertir el array de bytes en una imagen y guardarla
    img = Image.open(BytesIO(img_bytes))
    # Guardar la imagen en un archivo
    img.save(filename)

if __name__ == "__main__":
    load_dotenv()
    ip = os.getenv("SERVER_IP")
    port = int(os.getenv("SERVER_PORT"))
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Starting server udp..')
    while True:
        receive_image()
