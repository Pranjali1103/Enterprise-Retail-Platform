import pandas as pd
from pathlib import Path
import numpy as np

TRANSFORMED_DIR = Path("data/transformed")
TRANSFORMED_DIR.mkdir(parents=True, exist_ok=True)

# Read cleaned files
sales_df = pd.read_csv("data/cleaned/clean_sales.csv")
products_df = pd.read_csv("data/cleaned/cleaned_products.csv")
customers_df = pd.read_csv("data/cleaned/clean_customers.csv")
stores_df = pd.read_csv("data/cleaned/clean_stores.csv")
inventory_df = pd.read_csv("data/cleaned/cleaned_inventory.csv")


# Join files
df = sales_df.merge(products_df, on="product_id", how="left")
df = df.merge(customers_df, on="customer_id", how="left")
df = df.merge(stores_df, on="store_id", how="left")
df = df.merge(
    inventory_df,
    on=["product_id", "store_id"],
    how="left"
)

# Gross Amount
df["gross_amount"] = df["quantity"] * df["unit_price"]

# Discount Amount
df["discount_amount"] = (
    df["gross_amount"] * df["discount_percentage"] / 100
)

# Net Amount
df["net_amount"] = (
    df["gross_amount"] - df["discount_amount"]
)

# Sale Category
def sale_category(qty):
    if qty >= 50:
        return "Bulk Sale"
    elif qty >= 20:
        return "Medium Sale"
    else:
        return "Retail Sale"

df["sale_category"] = df["quantity"].apply(sale_category)

# Inventory Rule
df["available_quantity"] = (
    df["available_quantity"]
    - df["quantity"]
)

# No negative inventory
df["available_quantity"] = (
    df["available_quantity"].clip(lower=0)
)

# Inventory Status
df["inventory_status"] = np.where(
    df["available_quantity"] <= df["reorder_level"],
    "REORDER REQUIRED",
    "AVAILABLE"
)

# Save
df.to_csv(
    TRANSFORMED_DIR / "transformed_sales.csv",
    index=False
)

print("Transformation completed")
print(df.head())