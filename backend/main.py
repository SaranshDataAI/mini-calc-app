"""
FastAPI app entry point.

Why we don't use Python's eval() for the math: eval() would let anyone
send arbitrary code through the API and have your server execute it.
Instead we accept two numbers and an operator name, and only allow a
fixed set of operators. Slightly less flexible, much safer — and this
is exactly the tradeoff real APIs make.
"""

import math

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Calculator API")

# Allows the frontend (served from a different origin, e.g. opening
# index.html directly) to call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OPERATIONS = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
    "divide": lambda a, b: a / b,
    # Unary operator: b is ignored (kept only so the db row has a value).
    "sqrt": lambda a, b: math.sqrt(a),
}


@app.post("/calculate", response_model=schemas.CalculationResponse)
def calculate(request: schemas.CalculationRequest, db: Session = Depends(get_db)):
    if request.operator not in OPERATIONS:
        raise HTTPException(status_code=400, detail=f"Unknown operator: {request.operator}")

    if request.operator == "divide" and request.b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")

    if request.operator == "sqrt" and request.a < 0:
        raise HTTPException(status_code=400, detail="Cannot take square root of a negative number")

    result = OPERATIONS[request.operator](request.a, request.b)

    record = models.Calculation(
        a=request.a,
        b=request.b if request.operator != "sqrt" else 0,
        operator=request.operator,
        result=result,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@app.get("/history", response_model=List[schemas.CalculationResponse])
def get_history(db: Session = Depends(get_db)):
    return db.query(models.Calculation).order_by(models.Calculation.id.desc()).all()