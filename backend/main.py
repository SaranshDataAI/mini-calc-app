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

BASES = {
    "binary": 2,
    "octal": 8,
    "decimal": 10,
    "hexadecimal": 16,
}


def format_integer_in_base(value: int, base: int) -> str:
    """Return an integer as an uppercase, prefix-free representation in ``base``."""
    if value == 0:
        return "0"

    digits = "0123456789ABCDEF"
    sign = "-" if value < 0 else ""
    remaining = abs(value)
    converted_digits: list[str] = []

    while remaining:
        remaining, remainder = divmod(remaining, base)
        converted_digits.append(digits[remainder])

    return sign + "".join(reversed(converted_digits))


def parse_number_in_base(value: str, base: int) -> tuple[int, int]:
    """Parse a signed base-``base`` number into an exact numerator and denominator."""
    sign = -1 if value.startswith("-") else 1
    unsigned_value = value[1:] if value[:1] in "+-" else value

    if unsigned_value.count(".") > 1:
        raise ValueError("A number can contain only one decimal point.")

    whole_part, separator, fractional_part = unsigned_value.partition(".")
    if not whole_part and not fractional_part:
        raise ValueError("A number must contain at least one digit.")

    whole_value = int(whole_part or "0", base)
    if not separator:
        return sign * whole_value, 1

    fractional_value = int(fractional_part or "0", base)
    denominator = base ** len(fractional_part)
    return sign * (whole_value * denominator + fractional_value), denominator


def format_number_in_base(numerator: int, denominator: int, base: int) -> str:
    """Format an exact fraction, marking recurring fractional digits with parentheses."""
    digits = "0123456789ABCDEF"
    sign = "-" if numerator < 0 else ""
    whole_value, remainder = divmod(abs(numerator), denominator)
    result = sign + format_integer_in_base(whole_value, base)

    if remainder == 0:
        return result

    fractional_digits: list[str] = []
    remainder_positions: dict[int, int] = {}
    while remainder:
        if remainder in remainder_positions:
            repeat_start = remainder_positions[remainder]
            non_repeating = "".join(fractional_digits[:repeat_start])
            repeating = "".join(fractional_digits[repeat_start:])
            return f"{result}.{non_repeating}({repeating})"

        remainder_positions[remainder] = len(fractional_digits)
        remainder *= base
        digit, remainder = divmod(remainder, denominator)
        fractional_digits.append(digits[digit])

    return f"{result}.{''.join(fractional_digits)}"


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


@app.post("/convert", response_model=schemas.BaseConversionResponse)
def convert_base(request: schemas.BaseConversionRequest, db: Session = Depends(get_db)):
    """Convert a signed integer or fractional number between supported bases."""
    source_base = request.source_base.lower()
    target_base = request.target_base.lower()

    if source_base not in BASES or target_base not in BASES:
        supported_bases = ", ".join(BASES)
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported base. Choose one of: {supported_bases}.",
        )

    normalized_value = request.value.strip()
    if not normalized_value:
        raise HTTPException(status_code=400, detail="Enter a value to convert.")

    try:
        numerator, denominator = parse_number_in_base(
            normalized_value, BASES[source_base]
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"'{request.value}' is not a valid {source_base} number.",
        ) from exc

    conversion = models.BaseConversion(
        value=normalized_value.upper(),
        source_base=source_base,
        target_base=target_base,
        result=format_number_in_base(numerator, denominator, BASES[target_base]),
    )
    db.add(conversion)
    db.commit()
    db.refresh(conversion)

    return conversion


@app.get("/history", response_model=List[schemas.HistoryResponse])
def get_history(db: Session = Depends(get_db)):
    calculations = db.query(models.Calculation).all()
    conversions = db.query(models.BaseConversion).all()
    history = [
        {
            "id": item.id,
            "type": "calculation",
            "created_at": item.created_at,
            "a": item.a,
            "b": item.b,
            "operator": item.operator,
            "result": item.result,
        }
        for item in calculations
    ]
    history.extend(
        {
            "id": item.id,
            "type": "conversion",
            "created_at": item.created_at,
            "value": item.value,
            "source_base": item.source_base,
            "target_base": item.target_base,
            "result": item.result,
        }
        for item in conversions
    )
    return sorted(history, key=lambda item: item["created_at"], reverse=True)


@app.delete("/history")
def clear_history(db: Session = Depends(get_db)):
    deleted = db.query(models.Calculation).delete()
    deleted += db.query(models.BaseConversion).delete()
    db.commit()
    return {"message": "History cleared", "deleted": deleted}
