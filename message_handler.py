class MessageHandler:
    receiving_queue = []
    sending_queue = []

    @staticmethod
    def receive_from_central_repo(messages):
        """Receives multiple messages & adds them to queue."""
        MessageHandler.receiving_queue.extend(messages)

    @staticmethod
    def send_to_central_repo(message):
        """Sends processed message results to Central Repository."""
        MessageHandler.sending_queue.append(message)
