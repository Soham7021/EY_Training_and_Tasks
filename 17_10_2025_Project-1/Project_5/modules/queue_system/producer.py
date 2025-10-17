import time
import random
import pandas as pd
from queue import Queue
from pathlib import Path
from shipment_logger import logger

shipment_queue = Queue()

data_folder = Path(__file__).resolve().parent.parent / "data"
processed_csv = data_folder / "processed_shipments.csv"
shipments_df = pd.read_csv(processed_csv)

def push_updates():
    logger.info("Producer started pushing shipment updates...")
    for _, row in shipments_df.iterrows():
        message = {
            "ShipmentID": row["ShipmentID"],
            "Status": random.choice(["Dispatched", "In Transit", "Delivered"])
        }
        shipment_queue.put(message)
        logger.info(f"Pushed message: {message}")
        time.sleep(0.5)
    logger.info("All shipment messages pushed.")

if __name__ == "__main__":
    push_updates()


#
#
# import time
# import random
# from queue import Queue
# from pathlib import Path
# import pandas as pd
#
#
# shipment_queue = Queue()
#
# data_folder = Path(__file__).resolve().parent.parent / "data"
# processed_csv = data_folder / "processed_shipments.csv"
#
#
# shipments_df = pd.read_csv(processed_csv)
#
#
# def push_updates():
#     print("🚀 Producer started pushing shipment updates...")
#     for _, row in shipments_df.iterrows():
#         message = {
#             "ShipmentID": row["ShipmentID"],
#             "Status": random.choice(["Dispatched", "In Transit", "Delivered"])
#         }
#         shipment_queue.put(message)
#         print(f"📤 Pushed message: {message}")
#         time.sleep(0.5)
#
#     print("✅ All shipment messages pushed.")
#
# if __name__ == "__main__":
#     push_updates()
