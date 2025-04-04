import socket
import json

# Multiple messages to be processed
messages = [
    {"tags": ["tag1"], "body": "Message 1 word2"},
    {"tags": ["NOtag"], "body": "Message 2"},
    {"tags": ["tag4"], "body": "Message 3"},
    {"tags": ["Rtag3"], "body": "Message 4"},
    {"tags": ["tag2"], "body": "Message 5"}
]

# Send messages to the main server (localhost:5000)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect(("localhost", 5000))
    client_socket.sendall(json.dumps(messages).encode())
    print("✅ Test messages sent!")
