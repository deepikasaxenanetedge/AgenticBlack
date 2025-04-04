import socket
import json
import time
from message_handler import MessageHandler

class MessageAssembler:
    def __init__(self, port=6000):
        self.port = port

    def assemble_message(self, agent_tag, processed_result):
        """Joins tags & body to create final message."""
        return {"tags": [agent_tag], "body": processed_result}

    def send_to_central_repo(self):
        """Sends processed messages to Central Repo."""
        while True:
            if MessageHandler.sending_queue:
                message = MessageHandler.sending_queue.pop(0)

                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                        client_socket.connect(("localhost", self.port))
                        client_socket.sendall(json.dumps([message]).encode())
                        print(f"✅ Sent to Central Repo: {message}")
                except ConnectionRefusedError:
                    print("❌ Central Repository is unavailable.")
            time.sleep(1)

if __name__ == "__main__":
    assembler = MessageAssembler()
    assembler.send_to_central_repo()
