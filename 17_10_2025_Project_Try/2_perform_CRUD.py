import pandas as pd
import logging

logging.basicConfig(
    filename='data/file.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

product_df = pd.read_csv("data/products.csv")
warehouse_df = pd.read_csv("data/warehouse.csv")

def add_product():
    global product_df
    product_id = input("Enter ProductID: ")
    if product_df['ProductID'].astype(str).str.contains(product_id).any():
        print(f"Product with ID '{product_id}' already exists.")
        return
    name = input("Enter ProductName: ")
    category = input("Enter Category: ")
    try:
        price = float(input("Enter UnitPrice: "))
        if price <= 0:
            print("UnitPrice must be positive.")
            return
    except ValueError:
        print("Invalid price. Please enter a numeric value.")
        return
    new_product = {
        "ProductID": product_id,
        "ProductName": name,
        "Category": category,
        "UnitPrice": price
    }
    try:
        product_df = pd.concat([product_df, pd.DataFrame([new_product])], ignore_index=True)
        product_df.to_csv('data/products.csv', index=False)
        logging.info(f"Product with ID '{product_id}' has been added.")
    except Exception as e:
        logging.error(e)

def delete_product():
    global product_df
    product_id = input("Enter ProductID to delete: ")
    if product_id in product_df["ProductID"].astype(str).values:
        product_df = product_df[product_df["ProductID"] != product_id]
        product_df.to_csv('data/products.csv', index=False)
        print(f"Product {product_id} deleted successfully.")
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
    warehouse_id = input("Enter WarehouseID to update: ")
    if warehouse_id in warehouse_df["WarehouseID"].astype(str).values:
        try:
            new_capacity = int(input("Enter new Capacity: "))
            if new_capacity < 0:
                print("Capacity must be non-negative.")
                return
        except ValueError:
            print("Invalid capacity. Please enter an integer.")
            return
        warehouse_df.loc[warehouse_df["WarehouseID"] == warehouse_id, "Capacity"] = new_capacity
        warehouse_df.to_csv("data/warehouse.csv", index=False)
        print(f"Capacity of warehouse {warehouse_id} updated to {new_capacity}.")
    else:
        print(f"Warehouse {warehouse_id} not found.")

def main():
    while True:
        print("\n--- CRUD Operations Menu ---")
        print("1. Add a new product")
        print("2. Delete a product")
        print("3. Fetch all Electronics products")
        print("4. Update warehouse capacity")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

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
