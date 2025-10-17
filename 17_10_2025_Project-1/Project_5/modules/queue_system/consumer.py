import time
import pandas as pd
from pathlib import Path
from shipment_logger import logger
from producer import shipment_queue

data_folder = Path(__file__).resolve().parent.parent.parent / "data"
processed_csv = data_folder / "processed_shipments.csv"
shipments_df = pd.read_csv(processed_csv)

def process_updates():
    logger.info("Consumer started processing shipment updates...")
    start_time = time.time()

    while not shipment_queue.empty():
        message = shipment_queue.get()
        shipment_id = message["ShipmentID"]
        status = message["Status"]

        if shipment_id in shipments_df["ShipmentID"].values:
            shipments_df.loc[shipments_df["ShipmentID"] == shipment_id, "DeliveryStatus"] = status
            logger.info(f"Processed ShipmentID {shipment_id}, Status: {status}")
        else:
            logger.error(f"ShipmentID {shipment_id} not found in processed_shipments.csv")

        time.sleep(0.5)

    shipments_df.to_csv(processed_csv, index=False)
    logger.info(f"Updated processed shipments saved to {processed_csv}")

    end_time = time.time()
    logger.info(f"Consumer finished in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    process_updates()


#
#
#
# import time
# from queue import Queue
# from pathlib import Path
# import pandas as pd
#
# data_folder = Path(__file__).resolve().parent.parent / "data"
# processed_csv = data_folder / "processed_shipments.csv"
#
# shipments_df = pd.read_csv(processed_csv)
#
# from producer import shipment_queue
#
#
# def process_updates():
#     print("Consumer started processing shipment updates...")
#     while not shipment_queue.empty():
#         message = shipment_queue.get()
#         shipment_id = message["ShipmentID"]
#         status = message["Status"]
#
#         if shipment_id in shipments_df["ShipmentID"].values:
#             shipments_df.loc[shipments_df["ShipmentID"] == shipment_id, "DeliveryStatus"] = status
#             print(f"Processed ShipmentID {shipment_id}, Status: {status}")
#         else:
#             print(f"ShipmentID {shipment_id} not found in processed_shipments.csv")
#
#         time.sleep(0.5)
#
#
#     shipments_df.to_csv(processed_csv, index=False)
#     print(f"Updated processed shipments saved at {processed_csv}")
#
# if __name__ == "__main__":
#     process_updates()
