"""
Database models — the tables that actually exist in calculator.db.
"""

from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func

from database import Base


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    operator = Column(String, nullable=False)
    result = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BaseConversion(Base):
    __tablename__ = "base_conversions"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, nullable=False)
    source_base = Column(String, nullable=False)
    target_base = Column(String, nullable=False)
    result = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
