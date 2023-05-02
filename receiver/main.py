import threading
from dotenv import load_dotenv
import os
import logging
import sys
# Obtener el directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta del directorio superior
parent_dir = os.path.dirname(current_dir)

# Agregar la ruta del directorio superior a sys.path
sys.path.append(parent_dir)

from vault_codes.UdpServer import UDPServer
from vault_codes.customClasses import CustomPacket, UdpInfo

class Runner: 
    udpConnectionList = {}
    def __init__(self):
        pass
    def getudpConnectionList():
        return Runner.udpConnectionList
    
if __name__ == "__main__":
    load_dotenv()
    ip = os.getenv("SERVER_IP")
    min_port = int(os.getenv("MIN_PORT"))
    max_port = int(os.getenv("MAX_PORT"))
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Starting server udp..')
    image_dir = os.getenv("IMAGE_DIR")
    for port in range(min_port, max_port + 1):
        Runner.udpConnectionList[port] = UdpInfo()
        server = UDPServer(ip, port, image_dir, logging.getLogger('udpLogger'), Runner.udpConnectionList[port])
        logging.info(f'Starting server udp on port: {port}')
        t = threading.Thread(target=server.receive_image)
        t.start()
    
