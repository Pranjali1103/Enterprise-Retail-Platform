from sqlalchemy import Column, String, Float
from database.db import Base

class Product(Base):

    __tablename__ = "products"

    product_id = Column(String(20), primary_key=True)
    product_name = Column(String(100))
    category = Column(String(50))
    brand = Column(String(50))
    unit_price = Column(Float)
    supplier_id = Column(String(20))
    status = Column(String(20))
