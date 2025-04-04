import socket
import json
import threading
from message_handler import MessageHandler

class Server:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.queue = MessageHandler()

    def handle_client(self, client_socket, addr):
        """Handles incoming client messages."""
        data = client_socket.recv(4096).decode()
        if data:
            messages = json.loads(data)
            if isinstance(messages, list):
                self.queue.receive_from_central_repo(messages)
            else:
                self.queue.receive_from_central_repo([messages])
            print(f"📩 Received {len(messages)} messages from {addr}")
        client_socket.close()

    def start(self):
        """Starts the server to receive messages from Central Repo."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"🚀 Server listening on {self.host}:{self.port}...")

            while True:
                client_socket, addr = server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    server = Server()
    server.start()
