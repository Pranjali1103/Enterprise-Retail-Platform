from pathlib import Path
import pandas as pd


def inventory_extract() -> pd.DataFrame:

    inventory = pd.read_csv(
        "data/csv_files/inventory.csv",
        encoding="utf-8-sig"
    )

    print("\n========== Original Data ==========")
    print(inventory)

    inventory.columns = (
        inventory.columns
        .astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.replace("*", "", regex=False)
        .str.strip()
        .str.lower()
    )

    print("\nColumns of Inventory:", inventory.columns.to_list())

    return inventory


def clean_inventory(
    inventory: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:

    inventory_copy = inventory.copy()

    # ==========================
    # Rejected Records
    # ==========================

    rejected_inventory_id = inventory_copy[
        inventory_copy["inventory_id"].isna()
    ].copy()

    rejected_inventory_id["reject_reason"] = (
        "Missing Inventory ID"
    )

    rejected_product_id = inventory_copy[
        inventory_copy["product_id"].isna()
    ].copy()

    rejected_product_id["reject_reason"] = (
        "Missing Product ID"
    )

    rejected_store_id = inventory_copy[
        inventory_copy["store_id"].isna()
    ].copy()

    rejected_store_id["reject_reason"] = (
        "Missing Store ID"
    )

    rejected_quantity = inventory_copy[
        inventory_copy["available_quantity"] < 0
    ].copy()

    rejected_quantity["reject_reason"] = (
        "Invalid Available Quantity"
    )

    rejected_reorder_level = inventory_copy[
        inventory_copy["reorder_level"] < 0
    ].copy()

    rejected_reorder_level["reject_reason"] = (
        "Invalid Reorder Level"
    )

    rejected_duplicates = inventory_copy[
        inventory_copy.duplicated(
            subset=["inventory_id"],
            keep=False
        )
    ].copy()

    rejected_duplicates["reject_reason"] = (
        "Duplicate Inventory ID"
    )

    rejected_last_updated = inventory_copy[
        pd.to_datetime(
            inventory_copy["last_updated"],
            errors="coerce"
        ).isna()
    ].copy()

    rejected_last_updated["reject_reason"] = (
        "Invalid Last Updated Date"
    )

    # Combine Rejected Records

    rejected_inventory = pd.concat(
        [
            rejected_inventory_id,
            rejected_product_id,
            rejected_store_id,
            rejected_quantity,
            rejected_reorder_level,
            rejected_duplicates,
            rejected_last_updated
        ],
        ignore_index=True
    )

    rejected_inventory = (
        rejected_inventory
        .drop_duplicates()
    )

    # ==========================
    # Remove Invalid Records
    # ==========================

    duplicate_ids = (
        rejected_duplicates["inventory_id"]
        .dropna()
        .unique()
    )

    inventory_copy = inventory_copy[
        inventory_copy["inventory_id"].notna()
    ]

    inventory_copy = inventory_copy[
        inventory_copy["product_id"].notna()
    ]

    inventory_copy = inventory_copy[
        inventory_copy["store_id"].notna()
    ]

    inventory_copy = inventory_copy[
        inventory_copy["available_quantity"] >= 0
    ]

    inventory_copy = inventory_copy[
        inventory_copy["reorder_level"] >= 0
    ]

    inventory_copy = inventory_copy[
        pd.to_datetime(
            inventory_copy["last_updated"],
            errors="coerce"
        ).notna()
    ]

    # Remove ALL duplicate inventory IDs

    inventory_copy = inventory_copy[
        ~inventory_copy["inventory_id"].isin(
            duplicate_ids
        )
    ]

    # ==========================
    # Data Cleaning
    # ==========================

    inventory_copy["inventory_id"] = (
        inventory_copy["inventory_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    inventory_copy["product_id"] = (
        inventory_copy["product_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    inventory_copy["store_id"] = (
        inventory_copy["store_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    inventory_copy["available_quantity"] = (
        pd.to_numeric(
            inventory_copy["available_quantity"],
            errors="coerce"
        )
    )

    inventory_copy["reorder_level"] = (
        pd.to_numeric(
            inventory_copy["reorder_level"],
            errors="coerce"
        )
    )

    inventory_copy["last_updated"] = pd.to_datetime(
        inventory_copy["last_updated"],
        errors="coerce"
    )

    return inventory_copy, rejected_inventory


if __name__ == "__main__":

    Path("data/cleaned").mkdir(
        parents=True,
        exist_ok=True
    )

    Path("data/rejected").mkdir(
        parents=True,
        exist_ok=True
    )

    inventory = inventory_extract()

    cleaned_inventory, rejected_inventory = (
        clean_inventory(inventory)
    )

    print(
        "\n========== CLEANED INVENTORY =========="
    )
    print(cleaned_inventory)

    print(
        "\n========== REJECTED INVENTORY =========="
    )
    print(rejected_inventory)

    print(
        f"\nValid Records : {len(cleaned_inventory)}"
    )

    print(
        f"Rejected Records : {len(rejected_inventory)}"
    )

    cleaned_inventory.to_csv(
        "data/cleaned/cleaned_inventory.csv",
        index=False
    )

    rejected_inventory.to_csv(
        "data/rejected/rejected_inventory.csv",
        index=False
    )

    print("\nFiles Generated Successfully!")

    print(
        "\nCreated:\n"
        "data/cleaned/cleaned_inventory.csv\n"
        "data/rejected/rejected_inventory.csv"
    )