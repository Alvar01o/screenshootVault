import socket
import threading

class TCPServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def handle_client(self, client_socket, client_address):
        while True:
            command = client_socket.recv(1024).decode('utf-8')

            if not command:
                break

            print(f"Received command from {client_address}: {command}")

            if command == "comando1":
                response = self.funcion_comando1()
            elif command == "comando2":
                response = self.funcion_comando2()
            else:
                response = "Comando desconocido."

            client_socket.send(response.encode('utf-8'))

        client_socket.close()

    def funcion_comando1(self):
        return "Ejecutando función comando1"

    def funcion_comando2(self):
        return "Ejecutando función comando2"

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.ip, self.port))
        server_socket.listen(5)

        print(f"Server listening on {self.ip}:{self.port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_handler.start()

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 12345
    server = TCPServer(ip, port)
    server.start_server()
