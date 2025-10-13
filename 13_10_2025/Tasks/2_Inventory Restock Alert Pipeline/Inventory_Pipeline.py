import pandas as pd
import datetime as datetime

def run_pipeline():
    # Extract
    df = pd.read_csv('inventory.csv')

    # Transform
    df['RestockNeeded'] = df.apply(lambda x: 'Yes' if x['Quantity'] < x['ReorderLevel'] else 'No', axis=1)
    df['Totalvalue'] = df['Quantity'] * df['PricePerUnit']

    df.to_csv('restock_report.csv',index=False)
    print(f"Inventory pipeline completed at {datetime.datetime.now()}")

if __name__ == "__main__":
    run_pipeline()
