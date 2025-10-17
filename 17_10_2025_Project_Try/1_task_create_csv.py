import pandas as pd
import logging

logging.basicConfig(
    filename='data/file.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

product = {
    "ProductID": ["P101", "P102", "P103", "P104", "P105"],
    "ProductName": ["Laptop", "Mouse", "Keyboard", "Monitor", "Router"],
    "Category": ["Electronics", "Accessories", "Accessories", "Electronics", "Networking"],
    "UnitPrice": [800, 20, 35, 150, 90]
}
try:
    p_df = pd.DataFrame.from_dict(product)
    p_df.to_csv("data/products.csv", index=False)
    logging.info("Successfully created products.csv")
except Exception as e:
    logging.error(e)

warehouses_data = {
    "WarehouseID": ["W01", "W02", "W03"],
    "Location": ["Mumbai", "Delhi", "Chennai"],
    "Capacity": [1000, 800, 500]
}
try:
    w_df = pd.DataFrame.from_dict(warehouses_data)
    w_df.to_csv("data/warehouses.csv", index=False)
    logging.info("Successfully created warehouses.csv")
except Exception as e:
    logging.error(e)


shipment = {
    "ShipmentID": ["S001", "S002", "S003", "S004", "S005"],
    "ProductID": ["P101", "P102", "P103", "P104", "P105"],
    "WarehouseID": ["W01", "W02", "W01", "W03", "W02"],
    "Quantity": [100, 300, 150, 50, 200],
    "DispatchDate": ["2025-10-01", "2025-10-02", "2025-10-03", "2025-10-04", "2025-10-05"],
    "DeliveryDate": ["2025-10-05", "2025-10-06", "2025-10-08", "2025-10-09", "2025-10-12"]
}
try:
    s_df = pd.DataFrame.from_dict(shipment)
    s_df.to_csv("data/shipments.csv", index=False)
    logging.info("Successfully created shipments.csv")
except Exception as e:
    logging.error(e)
