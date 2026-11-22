import pandas as pd
from pathlib import Path


def store_extract_validate():

    stores = pd.read_csv(
        "data/stores.csv",
        encoding="utf-8-sig"
    )

    stores.columns = (
        stores.columns
        .astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
        .str.lower()
    )

    print("Columns:", stores.columns.to_list())

    stores_copy = stores.copy()

    # ==========================
    # Rejected Records
    # ==========================

    # Missing Store ID

    rejected_store_id = stores_copy[
        stores_copy["store_id"].isna()
    ].copy()

    rejected_store_id["rejection_reason"] = (
        "Missing Store ID"
    )

    # Missing Store Name

    rejected_store_name = stores_copy[
        stores_copy["store_name"].isna()
    ].copy()

    rejected_store_name["rejection_reason"] = (
        "Missing Store Name"
    )

    # Missing City

    rejected_city = stores_copy[
        stores_copy["city"].isna()
    ].copy()

    rejected_city["rejection_reason"] = (
        "Missing City"
    )

    # Duplicate Store ID

    rejected_duplicate = stores_copy[
        stores_copy.duplicated(
            subset=["store_id"],
            keep=False
        )
    ].copy()

    rejected_duplicate["rejection_reason"] = (
        "Duplicate Store ID"
    )

    # Combine All Rejected Records

    rejected_stores = pd.concat(
        [
            rejected_store_id,
            rejected_store_name,
            rejected_city,
            rejected_duplicate
        ],
        ignore_index=True
    )

    # ==========================
    # Save Rejected Records
    # ==========================

    rejected_path = Path(
        "data/rejected/stores"
    )

    rejected_path.mkdir(
        parents=True,
        exist_ok=True
    )

    rejected_stores.to_csv(
        rejected_path / "rejected_stores.csv",
        index=False
    )

    # ==========================
    # Remove Rejected Records
    # ==========================

    stores_copy = stores_copy[
        stores_copy["store_id"].notna()
    ]

    stores_copy = stores_copy[
        stores_copy["store_name"].notna()
    ]

    stores_copy = stores_copy[
        stores_copy["city"].notna()
    ]

    stores_copy = stores_copy.drop_duplicates(
        subset=["store_id"]
    )

    # ==========================
    # Cleaning / Transformation
    # ==========================

    stores_copy["store_name"] = (
        stores_copy["store_name"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    stores_copy["city"] = (
        stores_copy["city"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    stores_copy["state"] = (
        stores_copy["state"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    stores_copy["store_manager"] = (
        stores_copy["store_manager"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    stores_copy["status"] = (
        stores_copy["status"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    return stores_copy, rejected_stores


if __name__ == "__main__":

    valid_stores, rejected_stores = (
        store_extract_validate()
    )

    print("\nVALID STORES\n")
    print(valid_stores)

    print("\nREJECTED STORES\n")
    print(rejected_stores)

    print(f"\nValid Store Count: {len(valid_stores)}")
    print(f"Rejected Store Count: {len(rejected_stores)}")