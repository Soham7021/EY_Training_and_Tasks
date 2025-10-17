import os
import pandas as pd
import datetime
import schedule
import time

os.makedirs("daily_reports", exist_ok=True)

processed_csv = "data/processed_shipments.csv"
daily_folder = "daily_reports"


def generate_daily_summary():
    df = pd.read_csv(processed_csv, parse_dates=["DispatchDate", "DeliveryDate"])

    df["TotalValue"] = df["Quantity"] * df["UnitPrice"]
    df["DeliveryDays"] = (df["DeliveryDate"] - df["DispatchDate"]).dt.days

    today = pd.Timestamp.now().normalize()
    daily_df = df[df["DispatchDate"] == today]

    if daily_df.empty:
        print(f"No shipments dispatched on {today.date()}")
        return

    filename = f"daily_shipments_{today.strftime('%Y%m%d')}.csv"
    filepath = os.path.join(daily_folder, filename)
    daily_df.to_csv(filepath, index=False)

    print(f"Daily shipment summary saved: {filepath}")


schedule.every().day.at("17:04").do(generate_daily_summary)

print("Daily shipment scheduler running... Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(30)
