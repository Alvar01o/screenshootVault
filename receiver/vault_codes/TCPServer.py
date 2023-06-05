import socket
from bson.json_util import loads

class Server:
    def __init__(self, host, port, database_manager):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)

        self.database_manager = database_manager

    def run(self):
        client_socket, address = self.server_socket.accept()
        print(f"Connection from {address} has been established.")

        while True:
            command_data = client_socket.recv(1024).decode("utf-8")
            command_object = loads(command_data)

            # Save command to MongoDB
            self.database_manager.insert_command(command_object)

            # Create and send response
            response = Response("Command received", [], 100)
            client_socket.send(response.toJSON().encode("utf-8"))
