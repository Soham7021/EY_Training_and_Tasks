import pandas as pd
from datetime import datetime

def main():
    # Step 1: Extract
    products = pd.read_csv('products.csv')
    customers = pd.read_csv('customers.csv')
    orders = pd.read_csv('orders.csv')

    # Step 2.1: Join datasets
    merged = pd.merge(orders, customers, on='CustomerID', how='inner')
    merged = pd.merge(merged, products, on='ProductID', how='inner')

    # Step 2.2: Add calculated columns
    merged['TotalAmount'] = merged['Quantity'] * merged['Price']
    merged['OrderMonth'] = pd.to_datetime(merged['OrderDate']).dt.month

    # Step 2.3: Filter
    filtered = merged[(merged['Quantity'] >= 2) & (merged['Country'].isin(['India', 'UAE']))]

    # Step 2.4: Group and aggregate
    category_summary = filtered.groupby('Category')['TotalAmount'].sum().reset_index()
    segment_summary = filtered.groupby('Segment')['TotalAmount'].sum().reset_index()

    # Step 2.5: Sorting & Ranking
    customer_revenue = (
        filtered.groupby(['CustomerID', 'Name'])['TotalAmount']
        .sum()
        .reset_index()
        .sort_values(by='TotalAmount', ascending=False)
    )

    # Step 3: Load
    processed_orders = filtered[[
        'OrderID', 'CustomerID', 'Name', 'Country', 'Segment',
        'ProductName', 'Category', 'Quantity', 'Price', 'TotalAmount', 'OrderMonth'
    ]]
    processed_orders.to_csv('processed_orders.csv', index=False)
    category_summary.to_csv('category_summary.csv', index=False)
    segment_summary.to_csv('segment_summary.csv', index=False)

    # Print execution time
    print("Sales pipeline executed at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()