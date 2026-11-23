from sqlalchemy import Column, String, Date
from database.db import Base

class Customer(Base):

    __tablename__ = "customers"

    customer_id = Column(String(20), primary_key=True)
    customer_name = Column(String(100))
    email = Column(String(100))
    mobile = Column(String(20))
    city = Column(String(50))
    registration_date = Column(Date)
    customer_type = Column(String(50))