from pathlib import Path
from datetime import datetime
import pandas as pd
import schedule
import time


data_folder = Path("data")
processed_csv = data_folder / "processed_shipments.csv"


daily_reports_folder = data_folder / "daily_reports"
daily_reports_folder.mkdir(exist_ok=True)

def generate_daily_summary():
    today_str = datetime.now().strftime("%Y%m%d")
    daily_file = daily_reports_folder / f"daily_shipments_{today_str}.csv"


    df = pd.read_csv(processed_csv)


    df['DispatchDate'] = pd.to_datetime(df['DispatchDate'])
    df['DeliveryDate'] = pd.to_datetime(df['DeliveryDate'])


    if 'TotalValue' not in df.columns:
        df['TotalValue'] = df['Quantity'] * df['UnitPrice']
    if 'DeliveryDays' not in df.columns:
        df['DeliveryDays'] = (df['DeliveryDate'] - df['DispatchDate']).dt.days

    daily_summary = df.groupby('WarehouseID').agg(
        TotalShipments=('ShipmentID', 'count'),
        TotalQuantity=('Quantity', 'sum'),
        TotalValue=('TotalValue', 'sum'),
        AvgDeliveryDays=('DeliveryDays', 'mean')
    ).reset_index()


    daily_summary.to_csv(daily_file, index=False)
    print(f"✅ Daily shipment summary saved at: {daily_file}")


schedule.every().day.at("17:32").do(generate_daily_summary)

print("Scheduler started. Daily summary will run at 07:00 AM every day.")


while True:
    schedule.run_pending()
    time.sleep(60)
