from knowledge_source import KnowledgeSource

class SendingQueue:
    def __init__(self):
        self.queue = []
        self.knowledge_source = KnowledgeSource()

    def add_to_queue(self, message):
        self.queue.append(message)

    def process_and_send(self, message):
        tag = message.get("tag")
        body = message.get("body")

        result = self.knowledge_source.process_message(tag, body)
        self.add_to_queue(result)

        return result  # Sends result back to the server

if __name__ == "__main__":
    sq = SendingQueue()
    test_message = {"tag": "rule_1", "body": {"data": "sample"}}
    print(sq.process_and_send(test_message))
