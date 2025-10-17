from queue import Queue
from producer import push_updates
from consumer import process_updates
import os

os.makedirs("../data", exist_ok=True)

shipment_queue = Queue()

if __name__ == "__main__":
    push_updates(shipment_queue)
    process_updates(shipment_queue)
