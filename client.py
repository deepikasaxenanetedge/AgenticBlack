import json
from central_repository import CentralRepository

def send_messages():
    """Sends multiple messages to the central repository"""
    messages = [
        {"tags": ["tag1", "tag3"], "body": {"info": "Message 1"}},
        {"tags": ["tag2", "tag4"], "body": {"info": "Message 2"}},
        {"tags": ["tag1", "tag2"], "body": {"info": "Message 3"}}
    ]
    CentralRepository.store_results(messages)

if __name__ == "__main__":
    send_messages()




