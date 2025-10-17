# modules/queue_module/run_queue_demo.py
from producer import push_updates
from consumer import process_updates

if __name__ == "__main__":
    push_updates()
    process_updates()
