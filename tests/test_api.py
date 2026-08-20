"""
Tests for the calculator API.

Why test the API directly instead of the frontend: the frontend is just
a UI on top of this. If the API is correct, the frontend just has to
call it correctly — which is a much smaller thing to get wrong.
"""

import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add():
    response = client.post("/calculate", json={"a": 2, "b": 3, "operator": "add"})
    assert response.status_code == 200
    assert response.json()["result"] == 5


def test_divide_by_zero():
    response = client.post("/calculate", json={"a": 5, "b": 0, "operator": "divide"})
    assert response.status_code == 400


def test_unknown_operator():
    response = client.post("/calculate", json={"a": 1, "b": 1, "operator": "power"})
    assert response.status_code == 400


def test_sqrt():
    response = client.post("/calculate", json={"a": 9, "operator": "sqrt"})
    assert response.status_code == 200
    assert response.json()["result"] == 3


def test_sqrt_negative_number():
    response = client.post("/calculate", json={"a": -4, "operator": "sqrt"})
    assert response.status_code == 400


@pytest.mark.parametrize(
    ("value", "source_base", "target_base", "expected"),
    [
        ("11111111", "binary", "binary", "11111111"),
        ("11111111", "binary", "octal", "377"),
        ("11111111", "binary", "decimal", "255"),
        ("11111111", "binary", "hexadecimal", "FF"),
        ("377", "octal", "binary", "11111111"),
        ("377", "octal", "octal", "377"),
        ("377", "octal", "decimal", "255"),
        ("377", "octal", "hexadecimal", "FF"),
        ("255", "decimal", "binary", "11111111"),
        ("255", "decimal", "octal", "377"),
        ("255", "decimal", "decimal", "255"),
        ("255", "decimal", "hexadecimal", "FF"),
        ("FF", "hexadecimal", "binary", "11111111"),
        ("FF", "hexadecimal", "octal", "377"),
        ("FF", "hexadecimal", "decimal", "255"),
        ("FF", "hexadecimal", "hexadecimal", "FF"),
    ],
)
def test_all_base_conversion_combinations(value, source_base, target_base, expected):
    response = client.post(
        "/convert",
        json={"value": value, "source_base": source_base, "target_base": target_base},
    )
    assert response.status_code == 200
    assert response.json()["result"] == expected


def test_conversion_rejects_invalid_digit_for_source_base():
    response = client.post(
        "/convert",
        json={"value": "102", "source_base": "binary", "target_base": "octal"},
    )
    assert response.status_code == 400


def test_conversion_rejects_unsupported_base():
    response = client.post(
        "/convert",
        json={"value": "12", "source_base": "base12", "target_base": "decimal"},
    )
    assert response.status_code == 400


def test_history_returns_list():
    client.post("/calculate", json={"a": 1, "b": 1, "operator": "add"})
    response = client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_clear_history():
    client.post("/calculate", json={"a": 2, "b": 3, "operator": "add"})
    response = client.delete("/history")
    assert response.status_code == 200
    assert response.json()["message"] == "History cleared"
    assert client.get("/history").json() == []
