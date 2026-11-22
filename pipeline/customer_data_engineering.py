import pandas as pd
from pathlib import Path


def customer_extract_validate():

    customers = pd.read_csv(
        "data/csv_files/customers.csv",
        encoding="utf-8-sig"
    )

    customers.columns = (
        customers.columns
        .astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
        .str.lower()
    )

    customers_copy = customers.copy()

    # ======================
    # Rejected Records
    # ======================

    rejected_customer_id = customers_copy[
        customers_copy["customer_id"].isna()
    ].copy()

    rejected_customer_id[
        "rejection_reason"
    ] = "Missing Customer ID"

    rejected_customer_name = customers_copy[
        customers_copy["customer_name"].isna()
    ].copy()

    rejected_customer_name[
        "rejection_reason"
    ] = "Missing Customer Name"

    rejected_email = customers_copy[
        ~customers_copy["email"].astype(str).str.contains(
            r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
            regex=True,
            na=False
        )
    ].copy()

    rejected_email[
        "rejection_reason"
    ] = "Invalid Email"

    rejected_duplicate = customers_copy[
        customers_copy.duplicated(
            subset=["customer_id"],
            keep=False
        )
    ].copy()

    rejected_duplicate[
        "rejection_reason"
    ] = "Duplicate Customer ID"

    rejected_customers = pd.concat(
        [
            rejected_customer_id,
            rejected_customer_name,
            rejected_email,
            rejected_duplicate
        ],
        ignore_index=True
    )

    # ======================
    # Save Rejected Records
    # ======================

    rejected_path = Path(
        "data/rejected/customers"
    )

    rejected_path.mkdir(
        parents=True,
        exist_ok=True
    )

    rejected_customers.to_csv(
        rejected_path / "rejected_customers.csv",
        index=False
    )

    # ======================
    # Remove Rejected Records
    # ======================

    customers_copy = customers_copy[
        customers_copy["customer_id"].notna()
    ]

    customers_copy = customers_copy[
        customers_copy["customer_name"].notna()
    ]

    customers_copy = customers_copy[
        customers_copy["email"].astype(str).str.contains(
            r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
            regex=True,
            na=False
        )
    ]

    customers_copy = customers_copy.drop_duplicates(
        subset=["customer_id"]
    )

    # ======================
    # Cleaning / Transformation
    # ======================

    customers_copy["customer_name"] = (
        customers_copy["customer_name"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    customers_copy["email"] = (
        customers_copy["email"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    customers_copy["city"] = (
        customers_copy["city"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    customers_copy["customer_type"] = (
        customers_copy["customer_type"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # ======================
    # Save Clean Records
    # ======================

    cleaned_path = Path(
        "data/cleaned"
    )

    cleaned_path.mkdir(
        parents=True,
        exist_ok=True
    )

    customers_copy.to_csv(
        cleaned_path / "clean_customers.csv",
        index=False
    )

    return customers_copy, rejected_customers


if __name__ == "__main__":

    valid_customers, rejected_customers = (
        customer_extract_validate()
    )

    print("\nValid Customers")
    print(valid_customers)

    print("\nRejected Customers")
    print(rejected_customers)

    print(f"\nValid Count: {len(valid_customers)}")
    print(f"Rejected Count: {len(rejected_customers)}")