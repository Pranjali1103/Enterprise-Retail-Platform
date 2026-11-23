from sqlalchemy import Column, Integer, String, DateTime
from database.db import Base
from sqlalchemy.sql import func

class RejectedRecord(Base):

    __tablename__ = "rejected_records"

    id = Column(Integer, primary_key=True, autoincrement=True)

    source_file = Column(String(100))

    record_identifier = Column(String(100))

    rejection_reason = Column(String(255))

    created_at = Column(
        DateTime,
        default=func.now()
    )