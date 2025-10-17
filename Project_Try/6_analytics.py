import pandas as pd
import os


processed_csv = "data/processed_shipments.csv"
report_csv = "reports/logistics_analytics.csv"

df = pd.read_csv(processed_csv, parse_dates=["DispatchDate", "DeliveryDate"])

avg_delivery = df.groupby("WarehouseID")["DeliveryDays"].mean().reset_index()
avg_delivery.rename(columns={"DeliveryDays": "AvgDeliveryDays"}, inplace=True)


df["TotalValue"] = df["Quantity"] * df["UnitPrice"]
total_value_category = df.groupby("Category")["TotalValue"].sum().reset_index()
total_value_category.rename(columns={"TotalValue": "TotalShipmentValue"}, inplace=True)


df["Month"] = df["DispatchDate"].dt.to_period("M")
shipments_per_month = df.groupby("Month")["ShipmentID"].count().reset_index()
shipments_per_month.rename(columns={"ShipmentID": "NumShipments"}, inplace=True)


late_deliveries = df[df["DeliveryDays"] > 5][["ShipmentID", "WarehouseID", "DeliveryDays"]]


with open(report_csv, "w", newline="") as f:
    f.write("Average Delivery Time Per Warehouse\n")
    avg_delivery.to_csv(f, index=False)
    f.write("\nTotal Shipment Value Per Product Category\n")
    total_value_category.to_csv(f, index=False)
    f.write("\nNumber of Shipments Per Month\n")
    shipments_per_month.to_csv(f, index=False)
    f.write("\nLate Deliveries (DeliveryDays > 5)\n")
    late_deliveries.to_csv(f, index=False)

print(f"Analytics saved to {report_csv}")
