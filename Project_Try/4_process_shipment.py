import pandas as pd
import logging

logging.basicConfig(
    filename="data/file.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

products = pd.read_csv("data/products.csv")
warehouses = pd.read_csv("data/warehouse.csv")
shipments = pd.read_csv("data/shipments.csv")

merged = shipments.merge(products, on="ProductID", how="left")
merged = merged.merge(warehouses, on="WarehouseID", how="left")

if merged["ProductName"].isnull().any() or merged["Location"].isnull().any():
    missing_products = merged[merged["ProductName"].isnull()]["ProductID"].unique()
    missing_warehouses = merged[merged["Location"].isnull()]["WarehouseID"].unique()
    if len(missing_products) > 0:
        logging.error(f"Missing Product IDs: {missing_products}")
    if len(missing_warehouses) > 0:
        logging.error(f"Missing Warehouse IDs: {missing_warehouses}")

merged["TotalValue"] = merged["Quantity"] * merged["UnitPrice"]
merged["DispatchDate"] = pd.to_datetime(merged["DispatchDate"])
merged["DeliveryDate"] = pd.to_datetime(merged["DeliveryDate"])
merged["DeliveryDays"] = (merged["DeliveryDate"] - merged["DispatchDate"]).dt.days

merged.to_csv("data/processed_shipments.csv", index=False)
logging.info("Processed shipments saved to processed_shipments.csv")
