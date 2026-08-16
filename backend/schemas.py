"""
Pydantic schemas — define what valid input/output looks like.

Why separate from models.py: models.py describes the database table.
These describe the API contract. They usually match closely but are
kept separate on purpose — you don't always want to expose every DB
column to the outside world.
"""

from pydantic import BaseModel
from datetime import datetime


class CalculationRequest(BaseModel):
    a: float
    b: float
    operator: str  # one of: "add", "subtract", "multiply", "divide"


class CalculationResponse(BaseModel):
    id: int
    a: float
    b: float
    operator: str
    result: float
    created_at: datetime

    class Config:
        from_attributes = True  # lets this build directly from a Calculation object
