import threading
import server
import agent1
import agent2
import agent3
import central_repo
import message_assembler

def run():
    threading.Thread(target=central_repo.start_central_repo_server, daemon=True).start()
    threading.Thread(target=server.Server().start, daemon=True).start()
    
    threading.Thread(target=agent1.Agent(["tag1", "tag2", "tag3"], 5001).start, daemon=True).start()
    threading.Thread(target=agent2.Agent(["tag2", "tag3", "tag4"], 5002).start, daemon=True).start()
    threading.Thread(target=agent3.Agent(["tag3", "tag4", "tag1"], 5003).start, daemon=True).start()

    threading.Thread(target=message_assembler.MessageAssembler().send_to_central_repo, daemon=True).start()

    while True:
        pass

if __name__ == "__main__":
    run()
