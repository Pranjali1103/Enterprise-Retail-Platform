import pandas as pd


# --------------------------------------------------
# Gross Amount
# Gross Amount = Quantity × Unit Price
# --------------------------------------------------

def gross_amount(combined_data: pd.DataFrame) -> pd.DataFrame:

    combined_data["gross_amount"] = (
        combined_data["quantity"]
        * combined_data["unit_price"]
    )

    return combined_data


# --------------------------------------------------
# Discount Amount
# Discount Amount = Gross Amount × Discount %
# --------------------------------------------------

def discount_amount(combined_data: pd.DataFrame) -> pd.DataFrame:

    combined_data["discount_amount"] = (
        combined_data["gross_amount"]
        * combined_data["discount_percentage"]
        / 100
    )

    return combined_data


# --------------------------------------------------
# Net Amount = Gross Amount - Discount Amount
# --------------------------------------------------

def net_amount(combined_data: pd.DataFrame) -> pd.DataFrame:

    combined_data["net_amount"] = (
        combined_data["gross_amount"]
        - combined_data["discount_amount"]
    )

    return combined_data


# --------------------------------------------------
# Sale Category
# --------------------------------------------------

def sale_category(combined_data: pd.DataFrame) -> pd.DataFrame:

    combined_data["sale_category"] = (
        combined_data["quantity"]
        .apply(
            lambda quantity:
            "Bulk Sale"
            if quantity >= 50
            else (
                "Medium Sale"
                if quantity >= 20
                else "Retail Sale"
            )
        )
    )

    return combined_data


# --------------------------------------------------
# Update Inventory Quantity
# Available Quantity = Available Quantity - Quantity Sold
# --------------------------------------------------

def inventory_quantity(combined_data: pd.DataFrame) -> pd.DataFrame:

    combined_data["updated_available_quantity"] = (
        combined_data["available_quantity"]
        - combined_data["quantity"]
    )

    return combined_data


# --------------------------------------------------
# Prevent Negative Inventory
# --------------------------------------------------

def validate_inventory(combined_data: pd.DataFrame) -> pd.DataFrame:

    combined_data["updated_available_quantity"] = (
        combined_data["updated_available_quantity"]
        .clip(lower=0)
    )

    return combined_data


# --------------------------------------------------
# Inventory Status
# --------------------------------------------------

def inventory_status(combined_data: pd.DataFrame) -> pd.DataFrame:

    combined_data["inventory_status"] = (
        combined_data.apply(
            lambda row:
            "REORDER REQUIRED"
            if row["updated_available_quantity"]
            <= row["reorder_level"]
            else "AVAILABLE",
            axis=1
        )
    )

    return combined_data


# --------------------------------------------------
# Execute All Transformations
# --------------------------------------------------

def run_transformation(
    combined_data: pd.DataFrame
) -> pd.DataFrame:

    combined_data = gross_amount(
        combined_data
    )

    combined_data = discount_amount(
        combined_data
    )

    combined_data = net_amount(
        combined_data
    )

    combined_data = sale_category(
        combined_data
    )

    combined_data = inventory_quantity(
        combined_data
    )

    combined_data = validate_inventory(
        combined_data
    )

    combined_data = inventory_status(
        combined_data
    )

    return combined_data


# --------------------------------------------------
# Example Run
# --------------------------------------------------

if __name__ == "__main__":

    combined_data = pd.read_csv(
        "data/combined_data.csv"
    )

    transformed_data = run_transformation(
        combined_data
    )

    print(
        "\n========== TRANSFORMED DATA ==========\n"
    )

    print(transformed_data.head())

    transformed_data.to_csv(
        "data/transformed_data.csv",
        index=False
    )

    print(
        "\nTransformation Completed Successfully!"
    )

    print(
        "\nCreated:\n"
        "data/transformed_data.csv"
    )