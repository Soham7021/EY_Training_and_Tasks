from fastapi import FastAPI, HTTPException
import pandas as pd
from pathlib import Path


app = FastAPI(title="Supply Chain & Logistics API")


data_folder = Path(__file__).resolve().parent.parent.parent / "data"
products_csv = data_folder / "products.csv"
warehouses_csv = data_folder / "warehouses.csv"


products_df = pd.read_csv(products_csv)
warehouses_df = pd.read_csv(warehouses_csv)


@app.get("/products")
def get_products():
    return products_df.to_dict(orient="records")


@app.post("/products")
def add_product(product: dict):
    global products_df
    if product["ProductID"] in products_df["ProductID"].values:
        raise HTTPException(status_code=400, detail="ProductID already exists")
    products_df = pd.concat([products_df, pd.DataFrame([product])], ignore_index=True)
    products_df.to_csv(products_csv, index=False)
    return {"message": "Product added successfully", "product": product}


@app.put("/products/{product_id}")
def update_product(product_id: str, updated_data: dict):
    global products_df
    if product_id not in products_df["ProductID"].values:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in updated_data.items():
        if key in products_df.columns:
            products_df.loc[products_df["ProductID"] == product_id, key] = value
    products_df.to_csv(products_csv, index=False)
    return {"message": f"Product {product_id} updated successfully"}


@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    global products_df
    if product_id not in products_df["ProductID"].values:
        raise HTTPException(status_code=404, detail="Product not found")
    products_df = products_df[products_df["ProductID"] != product_id]
    products_df.to_csv(products_csv, index=False)
    return {"message": f"Product {product_id} deleted successfully"}



@app.get("/warehouses")
def get_warehouses():
    return warehouses_df.to_dict(orient="records")


@app.post("/warehouses")
def add_warehouse(warehouse: dict):
    global warehouses_df
    if warehouse["WarehouseID"] in warehouses_df["WarehouseID"].values:
        raise HTTPException(status_code=400, detail="WarehouseID already exists")
    warehouses_df = pd.concat([warehouses_df, pd.DataFrame([warehouse])], ignore_index=True)
    warehouses_df.to_csv(warehouses_csv, index=False)
    return {"message": "Warehouse added successfully", "warehouse": warehouse}


@app.put("/warehouses/{warehouse_id}")
def update_warehouse(warehouse_id: str, updated_data: dict):
    global warehouses_df
    if warehouse_id not in warehouses_df["WarehouseID"].values:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    for key, value in updated_data.items():
        if key in warehouses_df.columns:
            warehouses_df.loc[warehouses_df["WarehouseID"] == warehouse_id, key] = value
    warehouses_df.to_csv(warehouses_csv, index=False)
    return {"message": f"Warehouse {warehouse_id} updated successfully"}


@app.delete("/warehouses/{warehouse_id}")
def delete_warehouse(warehouse_id: str):
    global warehouses_df
    if warehouse_id not in warehouses_df["WarehouseID"].values:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    warehouses_df = warehouses_df[warehouses_df["WarehouseID"] != warehouse_id]
    warehouses_df.to_csv(warehouses_csv, index=False)
    return {"message": f"Warehouse {warehouse_id} deleted successfully"}
