from database.db import Base, engine

from models.product import Product
from models.store import Store
from models.customer import Customer
from models.sale import Sale
from models.inventory import Inventory
from models.rejected_record import RejectedRecord
from pipeline.pipeline_execution import PipelineExecution

Base.metadata.create_all(bind=engine)

print("Tables Created Successfully")