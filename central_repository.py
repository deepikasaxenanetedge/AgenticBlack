import json

class CentralRepository:
    repository = []

    @staticmethod
    def store_results(messages):
        """Stores multiple messages in JSON format"""
        CentralRepository.repository.extend(messages)
        print(f"Stored in Central Repository: {json.dumps(messages, indent=2)}")

    @staticmethod
    def get_messages(batch_size=5):
        """Retrieves multiple messages in JSON format"""
        if CentralRepository.repository:
            messages = CentralRepository.repository[:batch_size]
            CentralRepository.repository = CentralRepository.repository[batch_size:]
            return json.dumps(messages)
        return json.dumps([])


