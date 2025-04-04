from queue import Queue

class Queues:
    """Maintains separate receiving and sending queues for each agent"""
    
    # Receiving Queues (Messages coming from Message Handler)
    agent1_receive_queue = Queue()
    agent2_receive_queue = Queue()
    agent3_receive_queue = Queue()

    # Sending Queues (Processed messages to be sent back to Central Repository)
    agent1_send_queue = Queue()
    agent2_send_queue = Queue()
    agent3_send_queue = Queue()
