import time
import pandas as pd
import logging

logging.basicConfig(
    filename="../data/file.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

processed_csv = "../data/processed_shipments.csv"
shipments_df = pd.read_csv(processed_csv)

def process_updates(queue):
    logging.info("Consumer started processing shipment updates...")
    start_time = time.time()

    while not queue.empty():
        message = queue.get()
        shipment_id = message["ShipmentID"]
        status = message["Status"]

        if shipment_id in shipments_df["ShipmentID"].values:
            shipments_df.loc[shipments_df["ShipmentID"] == shipment_id, "DeliveryStatus"] = status
            logging.info(f"Processed ShipmentID {shipment_id}, Status: {status}")
        else:
            logging.error(f"ShipmentID {shipment_id} not found in processed_shipments.csv")

        time.sleep(0.5)

    shipments_df.to_csv(processed_csv, index=False)
    logging.info(f"Updated processed shipments saved to {processed_csv}")

    end_time = time.time()
    logging.info(f"Consumer finished in {end_time - start_time:.2f} seconds")
