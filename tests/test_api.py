"""
Tests for the calculator API.

Why test the API directly instead of the frontend: the frontend is just
a UI on top of this. If the API is correct, the frontend just has to
call it correctly — which is a much smaller thing to get wrong.
"""

import sys
import os

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


def test_history_returns_list():
    client.post("/calculate", json={"a": 1, "b": 1, "operator": "add"})
    response = client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
