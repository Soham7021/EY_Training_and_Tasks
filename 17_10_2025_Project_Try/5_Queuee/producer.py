import time
import pandas as pd
import logging
import random

logging.basicConfig(
    filename="../data/file.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

processed_csv = "../data/processed_shipments.csv"
shipments_df = pd.read_csv(processed_csv)

def push_updates(queue):
    logging.info("Producer started pushing shipment updates...")
    for _, row in shipments_df.iterrows():
        message = {
            "ShipmentID": row["ShipmentID"],
            "Status": random.choice(["Dispatched", "In Transit", "Delivered"])
        }
        queue.put(message)
        logging.info(f"Pushed message: {message}")
        time.sleep(0.5)
    logging.info("All shipment messages pushed.")
