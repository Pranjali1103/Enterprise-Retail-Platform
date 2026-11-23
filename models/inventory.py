from sqlalchemy import Column, String, Integer, Date, ForeignKey
from database.db import Base

class Inventory(Base):

    __tablename__ = "inventory"

    inventory_id = Column(String(20), primary_key=True)

    product_id = Column(
        String(20),
        ForeignKey("products.product_id")
    )

    store_id = Column(
        String(20),
        ForeignKey("stores.store_id")
    )

    available_quantity = Column(Integer)
    reorder_level = Column(Integer)
    last_updated = Column(Date)
