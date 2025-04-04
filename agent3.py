import socket
import json
import threading
from knowledge_source import KnowledgeSource
from message_handler import MessageHandler
from regulatory_layer import RegulatoryLayer  # ✅ Import Regulatory Layer

class Agent:
    def __init__(self, agent_tags, port):
        self.agent_tags = agent_tags
        self.port = port
        self.knowledge_source = KnowledgeSource()
        self.queue = MessageHandler()
        self.regulatory_layer = RegulatoryLayer()  # ✅ Initialize Regulatory Layer

    def process_messages(self):
        while True:
            if self.queue.receiving_queue:
                message = self.queue.receiving_queue.pop(0)
                tags, body = message["tags"], message["body"]

                if any(tag in self.agent_tags for tag in tags):  # ✅ Check tag
                    print(f"⚡ Agent3 Processing: {message}")

                    processed_body = self.knowledge_source.execute_rules(tags, body)

                    if processed_body is not None:
                        final_body = self.regulatory_layer.enforce_regulations(tags, processed_body)

                        if final_body is not None:
                            assembled_message = {"tags": tags, "body": final_body}
                            self.queue.send_to_central_repo(assembled_message)
                            print(f"✅ Sent to Central Repo: {assembled_message}")
                        else:
                            print(f"🚫 Message blocked by regulatory rules: {message}")
                    else:
                        print(f"🚫 Message discarded at agent level: {message}")

    def start(self):
        threading.Thread(target=self.process_messages, daemon=True).start()

if __name__ == "__main__":
    agent = Agent(["tag3", "tag4", "tag7"], 5003)
    agent.start()
