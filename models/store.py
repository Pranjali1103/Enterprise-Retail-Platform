from sqlalchemy import Column, String, Date
from database.db import Base

class Store(Base):

    __tablename__ = "stores"

    store_id = Column(String(20), primary_key=True)
    store_name = Column(String(100))
    city = Column(String(50))
    state = Column(String(50))
    store_manager = Column(String(100))
    opening_date = Column(Date)
    status = Column(String(20))
