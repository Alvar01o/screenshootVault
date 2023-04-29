import os
import socket
import struct
import progressbar
import time
from io import BytesIO
from datetime import datetime
from PIL import Image
from dotenv import load_dotenv

class UDPClient:
    def __init__(self) -> None:
        self.last_image_saved = None
        self.ip = ''
        self.port = ''
        load_dotenv()
        self.ip = os.getenv('SERVER_IP')
        self.port = int(os.getenv('SERVER_PORT'))

    def calculate_buffer_size(self, image_size_bytes):
        MIN_BUFFER_SIZE = 1024
        MAX_BUFFER_SIZE = 32768
        BUFFER_SIZE_FACTOR = 0.1
        buffer_size = int(image_size_bytes * BUFFER_SIZE_FACTOR)
        buffer_size = max(MIN_BUFFER_SIZE, buffer_size)
        buffer_size = min(MAX_BUFFER_SIZE, buffer_size)
        return buffer_size
    
    def set_last_image_saved(self, image_name):
        self.last_image_saved = image_name
    
    def get_last_image_saved(self):
        return self.last_image_saved

    def generate_file_name(self):
        d = datetime.today()
        self.last_image_saved = d.strftime("%d_%m_%Y-%H-%M-%S") + "_screenshot.png"
    
    def send_file(self):
        img = Image.open(self.get_last_image_saved())
        buf = BytesIO()
        img.save(buf, format='PNG')
        img_bytes = buf.getvalue()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        file_len = len(img_bytes)
        buffer_size = self.calculate_buffer_size(file_len)

        # Obtener el valor del hash SHA1
        api_key = os.getenv('API_KEY')

        # Enviar el nombre del archivo y el hash SHA1 como strings
        file_info = f"{self.get_last_image_saved()}|{api_key}"
        sock.sendto(file_info.encode('utf-8'), (self.ip, self.port))
        
        # Enviar el tamaño de la imagen como un entero (4 bytes)
        print(f"lenght :{file_len}")
        sock.sendto(struct.pack('<L', file_len), (self.ip, self.port))

        bar = progressbar.ProgressBar(max_value=file_len)

        for i in range(0, len(img_bytes), buffer_size):
            sock.sendto(img_bytes[i:i + buffer_size], (self.ip, self.port))
            time.sleep(0.1)  # Espera 0.1 segundos antes de enviar el siguiente paquete
            bar.update(i)
        bar.finish()
        sock.close()