import pandas as pd
from pathlib import Path

data_folder = Path(__file__).resolve().parent.parent.parent / "data"

products_csv = data_folder / "products.csv"
warehouses_csv = data_folder / "warehouses.csv"
shipments_csv = data_folder / "shipments.csv"
processed_csv = data_folder / "processed_shipments.csv"


products_df = pd.read_csv(products_csv)
warehouses_df = pd.read_csv(warehouses_csv)
shipments_df = pd.read_csv(shipments_csv)


merged_df = shipments_df.merge(products_df, on="ProductID", how="left")
merged_df = merged_df.merge(warehouses_df, on="WarehouseID", how="left")


merged_df["TotalValue"] = merged_df["Quantity"] * merged_df["UnitPrice"]


merged_df["DispatchDate"] = pd.to_datetime(merged_df["DispatchDate"])
merged_df["DeliveryDate"] = pd.to_datetime(merged_df["DeliveryDate"])


merged_df["DeliveryDays"] = (merged_df["DeliveryDate"] - merged_df["DispatchDate"]).dt.days


merged_df.to_csv(processed_csv, index=False)
print(f"Processed shipments saved at: {processed_csv}")
