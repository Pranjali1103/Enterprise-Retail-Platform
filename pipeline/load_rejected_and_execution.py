import pandas as pd
from pathlib import Path

from database.db import SessionLocal

from models.rejected_record import RejectedRecord
from models.pipeline_execution import PipelineExecution


def load_rejected_records():

    db = SessionLocal()

    files = [
        (
            "products.csv",
            "data/rejected/rejected_products.csv",
            "product_id"
        ),
        (
            "customers.csv",
            "data/rejected/rejected_customers.csv",
            "customer_id"
        ),
        (
            "stores.csv",
            "data/rejected/stores/rejected_stores.csv",
            "store_id"
        ),
        (
            "inventory.csv",
            "data/rejected/rejected_inventory.csv",
            "inventory_id"
        ),
        (
            "sales.csv",
            "data/rejected/rejected_sales.csv",
            "sale_id"
        )
    ]

    try:

        for source_file, file_path, key_column in files:

            if not Path(file_path).exists():
                print(f"File not found: {file_path}")
                continue

            df = pd.read_csv(file_path)

            for _, row in df.iterrows():

                rejected_record = RejectedRecord(
                    source_file=source_file,
                    record_identifier=str(
                        row.get(key_column, "")
                    ),
                    rejection_reason=row.get(
                        "rejection_reason",
                        "Unknown Reason"
                    )
                )

                db.add(rejected_record)

        db.commit()

        print("Rejected Records Loaded Successfully")

    except Exception as e:

        db.rollback()

        print("Error Loading Rejected Records:", e)

    finally:

        db.close()


def load_pipeline_execution():

    db = SessionLocal()

    try:

        execution = PipelineExecution(

            status="SUCCESS",

            products_received=10,

            stores_received=10,

            customers_received=10,

            sales_received=11,

            sales_loaded=11,

            sales_rejected=6,

            inventory_records=10,

            execution_time=5.0

        )
      
        db.add(execution)
        print({
    "status": execution.status,
    "products_received": execution.products_received,
    "stores_received": execution.stores_received,
    "customers_received": execution.customers_received,
    "sales_received": execution.sales_received,
    "sales_loaded": execution.sales_loaded,
    "sales_rejected": execution.sales_rejected,
    "inventory_records": execution.inventory_records,
    "execution_time": execution.execution_time
})

        db.commit()

        print("Pipeline Execution Loaded Successfully")

    except Exception as e:

        db.rollback()

        print("Error Loading Pipeline Execution:", e)

    finally:

        db.close()


if __name__ == "__main__":

    load_rejected_records()

    print("========================")
    load_pipeline_execution()