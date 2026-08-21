"""
Pydantic schemas — define what valid input/output looks like.

Why separate from models.py: models.py describes the database table.
These describe the API contract. They usually match closely but are
kept separate on purpose — you don't always want to expose every DB
column to the outside world.
"""

from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class CalculationRequest(BaseModel):
    a: float
    # Optional because unary operators (like "sqrt") only need `a`.
    # Defaults to 0 so it still has a value to store in the (non-nullable) db column.
    b: Optional[float] = 0
    operator: str  # one of: "add", "subtract", "multiply", "divide", "sqrt"


class CalculationResponse(BaseModel):
    id: int
    a: float
    b: float
    operator: str
    result: float
    created_at: datetime

    class Config:
        from_attributes = True  # lets this build directly from a Calculation object


class BaseConversionRequest(BaseModel):
    """Request for converting an integer between supported number bases."""

    value: str
    source_base: str
    target_base: str


class BaseConversionResponse(BaseModel):
    """A base-conversion result, represented as text to preserve all digits."""

    value: str
    source_base: str
    target_base: str
    result: str


class HistoryResponse(BaseModel):
    """A calculator or base-conversion entry in the shared history feed."""

    id: int
    type: str
    created_at: datetime
    a: Optional[float] = None
    b: Optional[float] = None
    operator: Optional[str] = None
    value: Optional[str] = None
    source_base: Optional[str] = None
    target_base: Optional[str] = None
    result: str | float
