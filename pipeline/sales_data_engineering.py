from pathlib import Path
import pandas as pd

# Directories
REJECTED_DIR = Path("data/rejected/sales")
CLEANED_DIR = Path("data/cleaned/sales")

# Create directories if they don't exist
REJECTED_DIR.mkdir(parents=True, exist_ok=True)
CLEANED_DIR.mkdir(parents=True, exist_ok=True)


def extract_sales():
    sales_df = pd.read_csv("data/csv_files/sales.csv")
    return sales_df


def clean_sales(sales_df):

    sales_df = sales_df.copy()

    sales_df.columns = (
        sales_df.columns
        .str.strip()
        .str.lower()
    )

    return sales_df


def validate_sales(sales_df):

    rejected_records = []

    # Missing Sale ID
    missing_sale_id = sales_df[sales_df["sale_id"].isna()].copy()
    missing_sale_id["rejection_reason"] = "Sale ID Missing"
    rejected_records.append(missing_sale_id)

    # Missing Product ID
    missing_product = sales_df[sales_df["product_id"].isna()].copy()
    missing_product["rejection_reason"] = "Product ID Missing"
    rejected_records.append(missing_product)

    # Missing Store ID
    missing_store = sales_df[sales_df["store_id"].isna()].copy()
    missing_store["rejection_reason"] = "Store ID Missing"
    rejected_records.append(missing_store)

    # Missing Customer ID
    missing_customer = sales_df[sales_df["customer_id"].isna()].copy()
    missing_customer["rejection_reason"] = "Customer ID Missing"
    rejected_records.append(missing_customer)

    # Invalid Quantity
    invalid_quantity = sales_df[sales_df["quantity"] <= 0].copy()
    invalid_quantity["rejection_reason"] = "Quantity must be greater than zero"
    rejected_records.append(invalid_quantity)

    # Duplicate Sale ID
    duplicate_sales = sales_df[
        sales_df.duplicated(subset=["sale_id"], keep=False)
    ].copy()

    duplicate_sales["rejection_reason"] = "Duplicate Sale ID"
    rejected_records.append(duplicate_sales)

    # Combine all rejected records
    rejected_df = pd.concat(rejected_records, ignore_index=True)

    return rejected_df


def create_clean_sales(sales_df):

    cleaned_df = sales_df.dropna(
        subset=[
            "sale_id",
            "product_id",
            "store_id",
            "customer_id"
        ]
    )

    cleaned_df = cleaned_df[
        cleaned_df["quantity"] > 0
    ]

    cleaned_df = cleaned_df[
        ~cleaned_df.duplicated(
            subset=["sale_id"],
            keep=False
        )
    ]

    return cleaned_df


def save_rejected_sales(rejected_df):

    rejected_df.to_csv(
        REJECTED_DIR / "rejected_sales.csv",
        index=False
    )


def save_clean_sales(cleaned_df):

    cleaned_df.to_csv(
        CLEANED_DIR / "clean_sales.csv",
        index=False
    )


if __name__ == "__main__":

    # Extract
    sales_df = extract_sales()
    print("===============ORIGINAL DATA=========================")
    print(sales_df)

    # Clean
    sales_df = clean_sales(sales_df)

    # Validate
    rejected_df = validate_sales(sales_df)

    # Create Clean Dataset
    cleaned_df = create_clean_sales(sales_df)

    # Save Files
    save_clean_sales(cleaned_df)
    save_rejected_sales(rejected_df)

    # Summary
    print("\n===== SALES VALIDATION SUMMARY =====")
    print("Valid Records   :", len(cleaned_df))
    print("Rejected Records:", len(rejected_df))

    print("\n=============== CLEANED DATA ================")
    print(cleaned_df)

    print("\n=============== REJECTED DATA ===============")
    print(rejected_df)