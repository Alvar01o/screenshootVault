import socket

class Client:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def send_command(self, command):
        self.client_socket.send(command.toJSON().encode("utf-8"))
        response_data = self.client_socket.recv(1024).decode("utf-8")
        return loads(response_data)
