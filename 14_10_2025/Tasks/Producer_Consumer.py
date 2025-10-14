import threading
import queue
import time
import random
import logging

# Setup logging
logging.basicConfig(
    filename='file1.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


q = queue.Queue()
lock = threading.Lock()
logging.info('Queue initiated')


def producer():
    try:
        for i in range(10):
            item = random.randint(1, 100)
            q.put(item)
            with lock:
                print(f"Producer: {item}")
                logging.info(f"Produced: {item}")
            time.sleep(1)
        q.put(None)
        with lock:
            print("Producer finished producing")
            logging.info('Producer finished producing')
    except Exception as e:
        with lock:
            logging.error(f"Producer error: {e}")


def consumer():
    try:
        while True:
            item = q.get()
            if item is None:
                break
            with lock:
                print(f"Consumed: {item}")
                logging.info(f"Consumed: {item}")
            time.sleep(2)
        q.put(None)
        with lock:
            print("Consumer finished consuming")
            logging.info('Consumer finished consuming')
    except Exception as e:
        with lock:
            logging.error(f"Consumer error: {e}")


producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()

with lock:
    print("Producer-Consumer thread finished")
    logging.info("Producer-Consumer thread finished")




