from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from database.db import Base

class Sale(Base):

    __tablename__ = "sales"

    sale_id = Column(String(20), primary_key=True)

    product_id = Column(
        String(20),
        ForeignKey("products.product_id")
    )

    store_id = Column(
        String(20),
        ForeignKey("stores.store_id")
    )

    customer_id = Column(
        String(20),
        ForeignKey("customers.customer_id")
    )

    quantity = Column(Integer)

    sale_date = Column(Date)

    discount_percentage = Column(Float)

    payment_mode = Column(String(50))
