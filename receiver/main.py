import threading
from dotenv import load_dotenv
import os
import logging
import sys
import signal

# Obtener el directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta del directorio superior
parent_dir = os.path.dirname(current_dir)

# Agregar la ruta del directorio superior a sys.path
sys.path.append(parent_dir)

from vault_codes.UdpServer import UDPServer
from vault_codes.customClasses import UdpInfo, TransferInfo

class Runner: 
    udpConnectionList = {}
    def __init__(self):
        pass

    def getudpConnectionList():
        return Runner.udpConnectionList
    
    @staticmethod
    def checkPort(port):
        if port in Runner.udpConnectionList:
            print(Runner.udpConnectionList[port])
        else :
            print("Port not used.")

    @staticmethod
    def checkPorts():
        for k, v in Runner.udpConnectionList.items():
            print(f"{k} : {v}")

servers = []

def stopServers():
    for server in servers:  # Assuming 'servers' is a list of your UDPServer instances
        if server.is_alive():
            server.stop()
    logging.info('All servers stopped.')

def startServer():
    for server in servers:  # Assuming 'servers' is a list of your UDPServer instances
        server.start()
    logging.info('All servers started.')

def signal_handler(sig, frame):
    logging.info('Stopping servers..')
    # Stop each server
    for server in servers:  # Assuming 'servers' is a list of your UDPServer instances
        server.stop()
    logging.info('All servers stopped.')
    sys.exit(0)  # exit the program
 
if __name__ == "__main__":
    load_dotenv()
    signal.signal(signal.SIGINT, signal_handler)
    ip = os.getenv("SERVER_IP")
    min_port = int(os.getenv("MIN_PORT"))
    max_port = int(os.getenv("MAX_PORT"))
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Starting udp Services.')
    image_dir = os.getenv("IMAGE_DIR")
    for port in range(min_port, max_port + 1):
        signal.signal(signal.SIGINT, signal_handler) #check
        #create connection information object
        currentThreadTransferenceInfo = UdpInfo() 
        Runner.udpConnectionList[port] = TransferInfo(TransferInfo.AVAILABLE,  currentThreadTransferenceInfo)
        #create server udp 
        server = UDPServer(ip, port, image_dir, logging.getLogger('udpLogger'), Runner.udpConnectionList[port])
        logging.info(f'Starting server udp on port: {port}')
        t = threading.Thread(target=server.receive_image)
        t.daemon = True
        t.start()
        servers.append(server)
#        t.join(60) #hilo vivira por 1 minuto.
    command = None 
    while command != 'exit' : 
        command = input()
        if command == 'stop-all':
            stopServers()
        if command == 'check-ports':
            Runner.checkPorts()
        
    

    #verificar el estado de los hilos.
    #si estan muertos revivirlos
    
    
