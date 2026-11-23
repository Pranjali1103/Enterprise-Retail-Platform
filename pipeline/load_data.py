import pandas as pd

from database.db import SessionLocal

from models.product import Product
from models.store import Store
from models.customer import Customer
from models.inventory import Inventory
from models.sale import Sale


def load_data():

    db = SessionLocal()

    try:

        # ======================
        # PRODUCTS
        # ======================

        products_df = pd.read_csv(
            "data/cleaned/cleaned_products.csv"
        )

        for _, row in products_df.iterrows():

            db.add(
                Product(
                    product_id=row["product_id"],
                    product_name=row["product_name"],
                    category=row["category"],
                    brand=row["brand"],
                    unit_price=row["unit_price"],
                    supplier_id=row["supplier_id"],
                    status=row["status"]
                )
            )

        print("Products Loaded")

        # ======================
        # STORES
        # ======================

        stores_df = pd.read_csv(
            "data/cleaned/clean_stores.csv"
        )

        for _, row in stores_df.iterrows():

            db.add(
                Store(
                    store_id=row["store_id"],
                    store_name=row["store_name"],
                    city=row["city"],
                    state=row["state"],
                    store_manager=row["store_manager"],
                    opening_date=row["opening_date"],
                    status=row["status"]
                )
            )

        print("Stores Loaded")

        # ======================
        # CUSTOMERS
        # ======================

        customers_df = pd.read_csv(
            "data/cleaned/clean_customers.csv"
        )

        for _, row in customers_df.iterrows():

            db.add(
                Customer(
                    customer_id=row["customer_id"],
                    customer_name=row["customer_name"],
                    email=row["email"],
                    mobile=row["mobile"],
                    city=row["city"],
                    registration_date=row["registration_date"],
                    customer_type=row["customer_type"]
                )
            )

        print("Customers Loaded")

        # Commit Parent Tables First
        db.commit()

        print("Products, Stores and Customers Loaded")

        # ======================
        # INVENTORY
        # ======================

        inventory_df = pd.read_csv(
            "data/cleaned/cleaned_inventory.csv"
        )

        for _, row in inventory_df.iterrows():

            db.add(
                Inventory(
                    inventory_id=row["inventory_id"],
                    product_id=row["product_id"],
                    store_id=row["store_id"],
                    available_quantity=row["available_quantity"],
                    reorder_level=row["reorder_level"],
                    last_updated=row["last_updated"]
                )
            )

        db.commit()

        print("Inventory Loaded Successfully")

        # ======================
        # SALES
        # ======================

        sales_df = pd.read_csv(
            "data/cleaned/clean_sales.csv"
        )

        # Get valid keys
        valid_products = set(products_df["product_id"])

        valid_stores = set(stores_df["store_id"])

        valid_customers = set(customers_df["customer_id"])

        # Keep only valid sales
        sales_df = sales_df[
            sales_df["product_id"].isin(valid_products)
        ]

        sales_df = sales_df[
            sales_df["store_id"].isin(valid_stores)
        ]

        sales_df = sales_df[
            sales_df["customer_id"].isin(valid_customers)
        ]

        print(
            "Valid Sales Records:",
            len(sales_df)
        )

        for _, row in sales_df.iterrows():

            db.add(
                Sale(
                    sale_id=row["sale_id"],
                    product_id=row["product_id"],
                    store_id=row["store_id"],
                    customer_id=row["customer_id"],
                    quantity=row["quantity"],
                    sale_date=row["sale_date"],
                    discount_percentage=row["discount_percentage"],
                    payment_mode=row["payment_mode"]
                )
            )

        db.commit()

        print("Sales Loaded Successfully")

        print("All Data Loaded Successfully")

    except Exception as e:

        db.rollback()

        print("Error:", e)

    finally:

        db.close()


if __name__ == "__main__":

    load_data()