import pandas as pd
from pathlib import Path

# ----------------------------
# Paths
# ----------------------------
data_folder = Path(__file__).resolve().parent.parent.parent / "data"
processed_csv = data_folder / "processed_shipments.csv"

reports_folder = Path(__file__).resolve().parent.parent.parent / "reports"
reports_folder.mkdir(exist_ok=True)  # create reports folder if it doesn't exist
report_file = reports_folder / "logistics_analytics.csv"

# ----------------------------
# Load processed shipments
# ----------------------------
df = pd.read_csv(processed_csv)

# Ensure date columns are datetime
df['DispatchDate'] = pd.to_datetime(df['DispatchDate'])
df['DeliveryDate'] = pd.to_datetime(df['DeliveryDate'])

# ----------------------------
# Prepare analytics rows
# ----------------------------
rows = []

# 1️⃣ Average delivery time per warehouse
avg_delivery_time = df.groupby('WarehouseID')['DeliveryDays'].mean()
for wid, days in avg_delivery_time.items():
    rows.append(["AvgDeliveryTime", wid, days, "days"])

# 2️⃣ Total shipment value per product category
total_value_category = df.groupby('Category')['TotalValue'].sum()
for cat, val in total_value_category.items():
    rows.append(["TotalValuePerCategory", cat, val, "currency"])

# 3️⃣ Number of shipments per month
df['Month'] = df['DispatchDate'].dt.to_period('M').astype(str)
shipments_per_month = df.groupby('Month').size()
for month, count in shipments_per_month.items():
    rows.append(["ShipmentsPerMonth", month, count, "shipments"])

# 4️⃣ Late deliveries (DeliveryDays > 5)
late_deliveries = df[df['DeliveryDays'] > 5]
for _, row in late_deliveries.iterrows():
    rows.append(["LateDelivery", row['ShipmentID'], row['DeliveryDays'], f"Warehouse={row['WarehouseID']}, Product={row['ProductID']}"])

# ----------------------------
# Save analytics to CSV
# ----------------------------
report_df = pd.DataFrame(rows, columns=["Metric", "Key", "Value", "ExtraInfo"])
report_df.to_csv(report_file, index=False)

print(f"✅ Logistics analytics report saved at: {report_file}")
