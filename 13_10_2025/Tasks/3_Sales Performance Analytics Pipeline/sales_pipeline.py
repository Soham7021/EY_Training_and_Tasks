import pandas as pd
import datetime as datetime
import logging
logging.basicConfig(
    filename='file.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_pipeline():
    logging.info("Pipeline started.")

    # Extract
    try:
        products = pd.read_csv('products.csv')
        orders = pd.read_csv('orders.csv')
        customers = pd.read_csv('customers.csv')
        logging.info('Extract done')
    except Exception as e:
        logging.error(f"Extraction failed: {e}")
        return

    # Transform 1
    try:
        merged = pd.merge(customers, orders, on='CustomerID', how='inner')
        merged = pd.merge(merged, products, on='ProductID', how='inner')
        logging.info('Merge done')
    except Exception as e:
        logging.error(f"Error during Joining: {e}")
        return

    # Transform 2
    try:
        merged['TotalAmount'] = merged['Quantity'] * merged['Price']
        merged['OrderMonth'] = pd.to_datetime(merged['OrderDate']).dt.month
        logging.info('Transform 2 done')
    except Exception as e:
        logging.error(f"Error during transformation: {e}")
        return

    # Transform 3
    try:
        filtered = merged[(merged['Quantity'] >= 2) & (merged['Country'].isin(['India', 'UAE']))]
        logging.info('Filter done')
    except Exception as e:
        logging.error(f"Error during filtering: {e}")
        return

    # Transform 4
    category_summary = filtered.groupby('Category')['TotalAmount'].sum().reset_index()
    segment_summary = filtered.groupby('Segment')['TotalAmount'].sum().reset_index()
    logging.info('Groupby done')

    # Transform 5
    customer_revenue = (
        filtered.groupby(['CustomerID', 'Name'])['TotalAmount']
        .sum()
        .reset_index()
        .sort_values(by='TotalAmount', ascending=False)
    )
    logging.info('Groupby done')

    # Load
    try:
        processed_orders = filtered[[
            'OrderID', 'CustomerID', 'Name', 'Country', 'Segment',
            'ProductName', 'Category', 'Quantity', 'Price', 'TotalAmount', 'OrderMonth'
        ]]
        processed_orders.to_csv('processed_orders.csv', index=False)
        category_summary.to_csv('category_summary.csv', index=False)
        segment_summary.to_csv('segment_summary.csv', index=False)
        logging.info('Load done')

    except Exception as e:
        logging.error(f"Error during processing: {e}")


if __name__ == '__main__':
    run_pipeline()