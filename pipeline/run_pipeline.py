import os

os.system("python -m pipeline.product_data_engineering")
os.system("python -m pipeline.customer_data_engineering")
os.system("python -m pipeline.store_data_engineering")
os.system("python -m pipeline.inventory_data_engineering")
os.system("python -m pipeline.sales_data_engineering")
os.system("python -m pipeline.transform_data")
os.system("python -m pipeline.load_rejected_and_execution")

print("\nPipeline Completed Successfully!")