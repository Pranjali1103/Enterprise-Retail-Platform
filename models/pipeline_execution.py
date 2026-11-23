from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)

from database.db import Base
from sqlalchemy.sql import func

class PipelineExecution(Base):

    __tablename__ = "pipeline_execution"

    execution_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    status = Column(String(20))

    products_received = Column(Integer)

    stores_received = Column(Integer)

    customers_received = Column(Integer)

    sales_received = Column(Integer)

    sales_loaded = Column(Integer)

    sales_rejected = Column(Integer)

    inventory_records = Column(Integer)

    execution_time = Column(Float)

    executed_at = Column(
        DateTime,
        default=func.now()
    )