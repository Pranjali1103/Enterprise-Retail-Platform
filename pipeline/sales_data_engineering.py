from pathlib import Path
import pandas as pd


# ==========================
# Directories
# ==========================

REJECTED_DIR = Path("data/rejected")
CLEANED_DIR = Path("data/cleaned")

REJECTED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

CLEANED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================
# Extract
# ==========================

def extract_sales() -> pd.DataFrame:

    sales_df = pd.read_csv(
        "data/csv_files/sales.csv",
        encoding="utf-8-sig"
    )

    return sales_df


# ==========================
# Clean Column Names
# ==========================

def clean_sales(
    sales_df: pd.DataFrame
) -> pd.DataFrame:

    sales_df = sales_df.copy()

    sales_df.columns = (
        sales_df.columns
        .astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
        .str.lower()
    )

    return sales_df


# ==========================
# Validate Sales
# ==========================

def validate_sales(
    sales_df: pd.DataFrame
) -> pd.DataFrame:

    rejected_records = []

    # Missing Sale ID
    missing_sale_id = sales_df[
        sales_df["sale_id"].isna()
    ].copy()

    missing_sale_id["rejection_reason"] = (
        "Missing Sale ID"
    )

    rejected_records.append(
        missing_sale_id
    )

    # Missing Product ID
    missing_product = sales_df[
        sales_df["product_id"].isna()
    ].copy()

    missing_product["rejection_reason"] = (
        "Missing Product ID"
    )

    rejected_records.append(
        missing_product
    )

    # Missing Store ID
    missing_store = sales_df[
        sales_df["store_id"].isna()
    ].copy()

    missing_store["rejection_reason"] = (
        "Missing Store ID"
    )

    rejected_records.append(
        missing_store
    )

    # Missing Customer ID
    missing_customer = sales_df[
        sales_df["customer_id"].isna()
    ].copy()

    missing_customer["rejection_reason"] = (
        "Missing Customer ID"
    )

    rejected_records.append(
        missing_customer
    )

    # Invalid Quantity
    invalid_quantity = sales_df[
        sales_df["quantity"] <= 0
    ].copy()

    invalid_quantity["rejection_reason"] = (
        "Invalid Quantity"
    )

    rejected_records.append(
        invalid_quantity
    )

    # Duplicate Sale ID
    duplicate_sales = sales_df[
        sales_df.duplicated(
            subset=["sale_id"],
            keep=False
        )
    ].copy()

    duplicate_sales["rejection_reason"] = (
        "Duplicate Sale ID"
    )

    rejected_records.append(
        duplicate_sales
    )

    rejected_df = pd.concat(
        rejected_records,
        ignore_index=True
    )

    rejected_df = rejected_df.drop_duplicates()

    return rejected_df


# ==========================
# Create Clean Dataset
# ==========================

def create_clean_sales(
    sales_df: pd.DataFrame
) -> pd.DataFrame:

    cleaned_df = sales_df.copy()

    cleaned_df = cleaned_df.dropna(
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

    # Remove ALL duplicate sale IDs
    cleaned_df = cleaned_df[
        ~cleaned_df.duplicated(
            subset=["sale_id"],
            keep=False
        )
    ]

    # Standardize IDs

    cleaned_df["sale_id"] = (
        cleaned_df["sale_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    cleaned_df["product_id"] = (
        cleaned_df["product_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    cleaned_df["store_id"] = (
        cleaned_df["store_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    cleaned_df["customer_id"] = (
        cleaned_df["customer_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    if "sale_date" in cleaned_df.columns:

        cleaned_df["sale_date"] = (
            pd.to_datetime(
                cleaned_df["sale_date"],
                errors="coerce"
            )
        )

    return cleaned_df


# ==========================
# Save Files
# ==========================

def save_rejected_sales(
    rejected_df: pd.DataFrame
) -> None:

    rejected_df.to_csv(
        REJECTED_DIR / "rejected_sales.csv",
        index=False
    )


def save_clean_sales(
    cleaned_df: pd.DataFrame
) -> None:

    cleaned_df.to_csv(
        CLEANED_DIR / "cleaned_sales.csv",
        index=False
    )


# ==========================
# Main
# ==========================

if __name__ == "__main__":

    sales_df = extract_sales()

    print(
        "\n========== ORIGINAL SALES =========="
    )

    print(sales_df)

    sales_df = clean_sales(
        sales_df
    )

    rejected_df = validate_sales(
        sales_df
    )

    cleaned_df = create_clean_sales(
        sales_df
    )

    save_clean_sales(
        cleaned_df
    )

    save_rejected_sales(
        rejected_df
    )

    print(
        "\n========== SALES VALIDATION SUMMARY =========="
    )

    print(
        f"Valid Records : {len(cleaned_df)}"
    )

    print(
        f"Rejected Records : {len(rejected_df)}"
    )

    print(
        "\n========== CLEANED SALES =========="
    )

    print(cleaned_df)

    print(
        "\n========== REJECTED SALES =========="
    )

    print(rejected_df)

    print(
        "\nFiles Generated Successfully!"
    )

    print(
        "\nCreated:\n"
        "data/cleaned/cleaned_sales.csv\n"
        "data/rejected/rejected_sales.csv"
    )