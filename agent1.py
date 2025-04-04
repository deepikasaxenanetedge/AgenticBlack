import socket
import json
import threading
from knowledge_source import KnowledgeSource
from message_handler import MessageHandler
from regulatory_layer import RegulatoryLayer

class Agent:
    def __init__(self, agent_tags, port):
        self.agent_tags = agent_tags
        self.port = port
        self.knowledge_source = KnowledgeSource()
        self.queue = MessageHandler()
        self.regulatory_layer = RegulatoryLayer()  # ✅ Initialize regulatory layer

    def process_messages(self):
        while True:
            if self.queue.receiving_queue:
                message = self.queue.receiving_queue.pop(0)
                tags, body = message["tags"], message["body"]

                if any(tag in self.agent_tags for tag in tags):  # ✅ Check if tag matches agent
                    print(f"⚡ Agent1 Processing: {message}")

                    # ✅ Step 1: Process through the Knowledge Source (Agent Rules)
                    processed_body = self.knowledge_source.execute_rules(tags, body)

                    if processed_body is not None:
                        # ✅ Step 2: Pass through the Regulatory Layer
                        final_body = self.regulatory_layer.enforce_regulations(tags, processed_body)

                        if final_body is not None:
                            # ✅ Step 3: Send to Central Repo if approved
                            assembled_message = {"tags": tags, "body": final_body}
                            self.queue.send_to_central_repo(assembled_message)
                            print(f"✅ Sent to Central Repo: {assembled_message} from agent1")
                        else:
                            print(f"🚫 Message blocked by regulatory rules: {message}")
                    else:
                        print(f"🚫 Message discarded at agent1 level: {message}")

    def start(self):
        threading.Thread(target=self.process_messages, daemon=True).start()

if __name__ == "__main__":
    agent = Agent(["tag1", "tag2", "tag3"], 5001)
    agent.start()
