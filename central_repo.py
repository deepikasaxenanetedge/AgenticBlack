import socket
import json
import threading

class CentralRepository:
    repository = []

    @staticmethod
    def store_results(messages):
        """Stores processed messages in JSON format."""
        CentralRepository.repository.extend(messages)
        print(f"📥 Stored in Central Repository: {json.dumps(messages, indent=2)}")

    @staticmethod
    def get_messages(batch_size=5):
        """Retrieves multiple messages."""
        if CentralRepository.repository:
            messages = CentralRepository.repository[:batch_size]
            CentralRepository.repository = CentralRepository.repository[batch_size:]
            return json.dumps(messages)
        return json.dumps([])

def start_central_repo_server(host="localhost", port=6000):
    """Starts the Central Repo server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"📡 Central Repository listening on {host}:{port}...")

        while True:
            client_socket, addr = server_socket.accept()
            with client_socket:
                data = client_socket.recv(4096).decode()
                if data:
                    messages = json.loads(data)
                    CentralRepository.store_results(messages)
                    print(f"📨 Received from {addr}: {messages}")

if __name__ == "__main__":
    start_central_repo_server()
