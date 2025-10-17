import pandas as pd


products_data = {
    "ProductID": ["P101", "P102", "P103", "P104", "P105"],
    "ProductName": ["Laptop", "Mouse", "Keyboard", "Monitor", "Router"],
    "Category": ["Electronics", "Accessories", "Accessories", "Electronics", "Networking"],
    "UnitPrice": [800, 20, 35, 150, 90]
}

products_df = pd.DataFrame(products_data)
products_df.to_csv("data/products.csv", index=False)



warehouses_data = {
    "WarehouseID": ["W01", "W02", "W03"],
    "Location": ["Mumbai", "Delhi", "Chennai"],
    "Capacity": [1000, 800, 500]
}

warehouses_df = pd.DataFrame(warehouses_data)
warehouses_df.to_csv("data/warehouses.csv", index=False)


# ---- SHIPMENTS DATA ----
shipments_data = {
    "ShipmentID": ["S001", "S002", "S003", "S004", "S005"],
    "ProductID": ["P101", "P102", "P103", "P104", "P105"],
    "WarehouseID": ["W01", "W02", "W01", "W03", "W02"],
    "Quantity": [100, 300, 150, 50, 200],
    "DispatchDate": ["2025-10-01", "2025-10-02", "2025-10-03", "2025-10-04", "2025-10-05"],
    "DeliveryDate": ["2025-10-05", "2025-10-06", "2025-10-08", "2025-10-09", "2025-10-12"]
}

shipments_df = pd.DataFrame(shipments_data)
shipments_df.to_csv("data/shipments.csv", index=False)


print("All CSV files created successfully in the 'data' folder!")
