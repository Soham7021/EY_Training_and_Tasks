import pandas as pd
from pathlib import Path

data_folder = Path(__file__).resolve().parent.parent.parent / "data"
data_folder.mkdir(parents=True, exist_ok=True)  # Ensure data folder exists

products_csv = data_folder / "products.csv"
warehouses_csv = data_folder / "warehouses.csv"

if products_csv.exists():
    products_df = pd.read_csv(products_csv)
else:
    products_df = pd.DataFrame(columns=["ProductID", "ProductName", "Category", "UnitPrice"])

if warehouses_csv.exists():
    warehouses_df = pd.read_csv(warehouses_csv)
else:
    warehouses_df = pd.DataFrame(columns=["WarehouseID", "Location", "Capacity"])



def add_product():
    global products_df
    product_id = input("Enter ProductID: ")
    name = input("Enter ProductName: ")
    category = input("Enter Category: ")
    price = float(input("Enter UnitPrice: "))
    new_product = {
        "ProductID": product_id,
        "ProductName": name,
        "Category": category,
        "UnitPrice": price
    }
    products_df = pd.concat([products_df, pd.DataFrame([new_product])], ignore_index=True)
    products_df.to_csv(products_csv, index=False)
    print(f"Product {name} added successfully.")


def delete_product():
    global products_df
    product_id = input("Enter ProductID to delete: ")
    if product_id in products_df["ProductID"].values:
        products_df = products_df[products_df["ProductID"] != product_id]
        products_df.to_csv(products_csv, index=False)
        print(f"Product {product_id} deleted successfully.")
    else:
        print(f"Product {product_id} not found.")


def fetch_electronics():
    electronics = products_df[products_df["Category"] == "Electronics"]
    if electronics.empty:
        print("No Electronics products found.")
    else:
        print("\n📦 Electronics Products:")
        print(electronics)


def update_capacity():
    global warehouses_df
    warehouse_id = input("Enter WarehouseID to update: ")
    if warehouse_id in warehouses_df["WarehouseID"].values:
        new_capacity = int(input("Enter new Capacity: "))
        warehouses_df.loc[warehouses_df["WarehouseID"] == warehouse_id, "Capacity"] = new_capacity
        warehouses_df.to_csv(warehouses_csv, index=False)
        print(f"Capacity of warehouse {warehouse_id} updated to {new_capacity}.")
    else:
        print(f"Warehouse {warehouse_id} not found.")



def main_menu():
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
            fetch_electronics()
        elif choice == "4":
            update_capacity()
        elif choice == "5":
            print("Exiting CRUD menu. Goodbye! 👋")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main_menu()
