import csv
import logging
import pandas as pd

data = {
    'product': ['Laptop', 'Mouse', 'Keyboard'],
    'price': [70000, 500, 1200],
    'quantity': [2, 5, 3]
}

df = pd.DataFrame(data)
df.to_csv('csv_task.csv', index=False)

logging.basicConfig(
    filename='sales.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:

    with open('csv_task.csv', 'r') as file:
        reader = csv.DictReader(file)

        for i in reader:
            try:
                product = i['product']
                price = float(i['price'])
                quantity = int(i['quantity'])
                total = price * quantity
                print(f"{product} total = {int(total)}")
                logging.info(f"{product} total sales = {int(total)}")
            except ValueError:
                logging.error(f"Invalid value in row: {i}")
except FileNotFoundError:
    logging.error("file not found.")