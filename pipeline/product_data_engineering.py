from pathlib import Path
import pandas as pd


def product_extract() -> pd.DataFrame:

    products = pd.read_csv(
        "data/Products.csv",
        encoding="utf-8-sig"
    )

    print("\n========== Original Data ==========")
    print(products)

    products.columns = (
        products.columns
        .astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
        .str.lower()
    )

    print("\nColumns of Products:", products.columns.to_list())

    return products


def clean_products(products: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:

    products_copy = products.copy()



    rejected_product_id = products_copy[
        products_copy["product_id"].isna()
    ].copy()

    rejected_product_id["reject_reason"] = "Missing Product ID"

    rejected_product_name = products_copy[
        products_copy["product_name"].isna()
    ].copy()

    rejected_product_name["reject_reason"] = "Missing Product Name"

    rejected_price = products_copy[
        products_copy["unit_price"] <= 0
    ].copy()

    rejected_price["reject_reason"] = "Invalid Unit Price"

    rejected_duplicates = products_copy[
        products_copy.duplicated(
            subset=["product_id"],
            keep=False
        )
    ].copy()

    rejected_duplicates["reject_reason"] = "Duplicate Product ID"

    # Combine all rejected records

    rejected_products = pd.concat(
        [
            rejected_product_id,
            rejected_product_name,
            rejected_price,
            rejected_duplicates
        ],
        ignore_index=True
    )

    # Remove duplicate rejected rows

    rejected_products = rejected_products.drop_duplicates()

    # -------------------------
    # Remove Invalid Records
    # -------------------------

    products_copy = products_copy[
        products_copy["product_id"].notna()
    ]

    products_copy = products_copy[
        products_copy["product_name"].notna()
    ]

    products_copy = products_copy[
        products_copy["unit_price"] > 0
    ]

    products_copy = products_copy.drop_duplicates(
        subset=["product_id"]
    )

    # -------------------------
    # Data Cleaning
    # -------------------------

    products_copy["product_name"] = (
        products_copy["product_name"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    products_copy["category"] = (
        products_copy["category"]
        .fillna("Unknown Category")
        .astype(str)
        .str.strip()
        .str.title()
    )

    products_copy["brand"] = (
        products_copy["brand"]
        .fillna("Unknown Brand")
        .astype(str)
        .str.strip()
        .str.title()
    )

    products_copy["supplier_id"] = (
        products_copy["supplier_id"]
        .fillna("Unknown Supplier")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    products_copy["status"] = (
        products_copy["status"]
        .fillna("Active")
        .astype(str)
        .str.strip()
        .str.title()
    )

    return products_copy, rejected_products


if __name__ == "__main__":

    

    Path("data/cleaned").mkdir(
        parents=True,
        exist_ok=True
    )

    Path("data/rejected").mkdir(
        parents=True,
        exist_ok=True
    )

    products = product_extract()

    cleaned_products, rejected_products = clean_products(
        products
    )

    print("\n========== CLEANED PRODUCTS ==========")
    print(cleaned_products)

    print("\n========== REJECTED PRODUCTS ==========")
    print(rejected_products)

    print(f"\nValid Records    : {len(cleaned_products)}")
    print(f"Rejected Records : {len(rejected_products)}")

    # Save cleaned data

    cleaned_products.to_csv(
        "data/cleaned/cleaned_products.csv",
        index=False
    )

    # Save rejected data

    rejected_products.to_csv(
        "data/rejected/rejected_products.csv",
        index=False
    )

    print("\nFiles Generated Successfully!")

    print(
        "\nCreated:\n"
        "data/cleaned/cleaned_products.csv\n"
        "data/rejected/rejected_products.csv"
    )