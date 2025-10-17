from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import pandas as pd
import logging

logging.basicConfig(
    filename='data/file.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

product_df = pd.read_csv("data/products.csv")
warehouse_df = pd.read_csv("data/warehouse.csv")

class Product(BaseModel):
    ProductID: str
    ProductName: str
    Category: str
    UnitPrice: float

    @field_validator("UnitPrice")
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("UnitPrice must be positive")
        return v

class Warehouse(BaseModel):
    WarehouseID: str
    Location: str
    Capacity: int

    @field_validator("Capacity")
    @classmethod
    def capacity_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Capacity must be non-negative")
        return v

@app.get("/products")
def get_products():
    return product_df.to_dict(orient="records")

@app.post("/products")
def add_product(product: Product):
    global product_df
    if product.ProductID in product_df["ProductID"].astype(str).values:
        raise HTTPException(status_code=400, detail="Product already exists")
    new_row = pd.DataFrame([product.model_dump()])
    product_df = pd.concat([product_df, new_row], ignore_index=True)
    product_df.to_csv("data/products.csv", index=False)
    logging.info(f"Product '{product.ProductID}' added successfully.")
    return {"message": f"Product '{product.ProductID}' added successfully."}

@app.put("/products/{product_id}")
def update_product(product_id: str, updated_product: Product):
    global product_df
    if product_id not in product_df["ProductID"].astype(str).values:
        raise HTTPException(status_code=404, detail="Product not found")
    product_df.loc[product_df["ProductID"] == product_id, ["ProductID", "ProductName", "Category", "UnitPrice"]] = [
        [updated_product.ProductID, updated_product.ProductName, updated_product.Category, updated_product.UnitPrice]
    ]
    product_df.to_csv("data/products.csv", index=False)
    logging.info(f"Product '{product_id}' updated successfully.")
    return {"message": f"Product '{product_id}' updated successfully."}

@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    global product_df
    if product_id not in product_df["ProductID"].astype(str).values:
        raise HTTPException(status_code=404, detail="Product not found")
    product_df = product_df[product_df["ProductID"] != product_id]
    product_df.to_csv("data/products.csv", index=False)
    logging.info(f"Product '{product_id}' deleted successfully.")
    return {"message": f"Product '{product_id}' deleted successfully."}

@app.get("/warehouses")
def get_warehouses():
    return warehouse_df.to_dict(orient="records")

@app.post("/warehouses")
def add_warehouse(warehouse: Warehouse):
    global warehouse_df
    if warehouse.WarehouseID in warehouse_df["WarehouseID"].astype(str).values:
        raise HTTPException(status_code=400, detail="Warehouse already exists")
    new_row = pd.DataFrame([warehouse.model_dump()])
    warehouse_df = pd.concat([warehouse_df, new_row], ignore_index=True)
    warehouse_df.to_csv("data/warehouse.csv", index=False)
    logging.info(f"Warehouse '{warehouse.WarehouseID}' added successfully.")
    return {"message": f"Warehouse '{warehouse.WarehouseID}' added successfully."}

@app.put("/warehouses/{warehouse_id}")
def update_warehouse(warehouse_id: str, updated_warehouse: Warehouse):
    global warehouse_df
    if warehouse_id not in warehouse_df["WarehouseID"].astype(str).values:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    warehouse_df.loc[warehouse_df["WarehouseID"] == warehouse_id, ["WarehouseID", "Location", "Capacity"]] = [
        [updated_warehouse.WarehouseID, updated_warehouse.Location, updated_warehouse.Capacity]
    ]
    warehouse_df.to_csv("data/warehouse.csv", index=False)
    logging.info(f"Warehouse '{warehouse_id}' updated successfully.")
    return {"message": f"Warehouse '{warehouse_id}' updated successfully."}

@app.delete("/warehouses/{warehouse_id}")
def delete_warehouse(warehouse_id: str):
    global warehouse_df
    if warehouse_id not in warehouse_df["WarehouseID"].astype(str).values:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    warehouse_df = warehouse_df[warehouse_df["WarehouseID"] != warehouse_id]
    warehouse_df.to_csv("data/warehouse.csv", index=False)
    logging.info(f"Warehouse '{warehouse_id}' deleted successfully.")
    return {"message": f"Warehouse '{warehouse_id}' deleted successfully."}
