import pandas as pd
import logging
from pydantic import BaseModel, validator


logging.basicConfig(
    filename='data/file.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class Product(BaseModel):
    product_id: str
    name: str
    category: str
    price: float

    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('UnitPrice must be positive')
        return v


class Warehouse(BaseModel):
    warehouse_id: str
    capacity: int


product_df = pd.read_csv("data/products.csv")
warehouse_df = pd.read_csv("data/warehouse.csv")



def add_product():
    global product_df
    product_id = input("Enter ProductID: ").strip()

    if product_df['ProductID'].astype(str).str.contains(product_id).any():
        print(f"Product with ID '{product_id}' already exists.")
        return

    name = input("Enter ProductName: ").strip()
    category = input("Enter Category: ").strip()

    try:
        price = float(input("Enter UnitPrice: ").strip())
        product = Product(product_id=product_id, name=name, category=category, price=price)
    except ValueError as e:
        print(f"Error: {e}")
        return

    new_product = {
        "ProductID": product.product_id,
        "ProductName": product.name,
        "Category": product.category,
        "UnitPrice": product.price
    }

    try:
        product_df = pd.concat([product_df, pd.DataFrame([new_product])], ignore_index=True)
        product_df.to_csv('data/products.csv', index=False)
        logging.info(f"Product with ID '{product_id}' has been added.")
        print(f"Product '{name}' added successfully!")
    except Exception as e:
        logging.error(f"Failed to add product: {e}")


def delete_product():
    global product_df
    product_id = input("Enter ProductID to delete: ").strip()

    if product_id in product_df["ProductID"].astype(str).values:
        product_df = product_df[product_df["ProductID"] != product_id]
        product_df.to_csv('data/products.csv', index=False)
        print(f"Product {product_id} deleted successfully.")
        logging.info(f"Product {product_id} deleted.")
    else:
        print(f"Product {product_id} not found.")


def fetch_electronic_product():
    electronics = product_df[product_df["Category"].str.lower() == "electronics"]
    if electronics.empty:
        print("No Electronics products found.")
    else:
        print("Electronics Products:")
        print(electronics)


def update_warehouse():
    global warehouse_df
    warehouse_id = input("Enter WarehouseID to update: ").strip()

    if warehouse_id in warehouse_df["WarehouseID"].astype(str).values:
        try:
            new_capacity = int(input("Enter new Capacity: ").strip())
            warehouse = Warehouse(warehouse_id=warehouse_id, capacity=new_capacity)
        except ValueError:
            print("Invalid capacity. Please enter an integer.")
            return

        warehouse_df.loc[warehouse_df["WarehouseID"] == warehouse.warehouse_id, "Capacity"] = warehouse.capacity
        warehouse_df.to_csv("data/warehouse.csv", index=False)
        print(f"Capacity of warehouse {warehouse_id} updated to {warehouse.capacity}.")
        logging.info(f"Warehouse {warehouse_id} capacity updated.")
    else:
        print(f"Warehouse {warehouse_id} not found.")


# --- Main Menu ---
def main():
    while True:
        print("\n--- CRUD Operations Menu ---")
        print("1. Add a new product")
        print("2. Delete a product")
        print("3. Fetch all Electronics products")
        print("4. Update warehouse capacity")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_product()
        elif choice == "2":
            delete_product()
        elif choice == "3":
            fetch_electronic_product()
        elif choice == "4":
            update_warehouse()
        elif choice == "5":
            print("Thank you for using our application. See you soon!")
            break
        else:
            print("Please enter a valid choice.")


if __name__ == '__main__':
    main()
