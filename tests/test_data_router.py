import sys
import os
import csv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from routes.data import data_router
from models import FilterParams

app = FastAPI()
app.include_router(data_router)
client = TestClient(app)

def load_alerts_csv():
    path = os.path.join(os.path.dirname(__file__), '..', 'tv_alerts.csv')
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def test_normalize_filters_endpoint():
    payload = {
        "start_time": "9:03",
        "end_time": "16:00",
        "days": ["Mon", "Tue"],
        "weeks": [1, 2],
        "start_date": "2025-07-01",
        "end_date": "2025-07-31"
    }
    response = client.post("/data/filters/normalize", json=payload)
    print("Response status:", response.status_code)
    print("Response body:", response.text)
    assert response.status_code == 200
    data = response.json()
    assert data["start_time"] == "09:03"
    assert data["end_time"] == "16:00"
    assert data["days"] == ["mon", "tue"]
    assert data["weeks"] == [1, 2]
    assert data["start_date"] == "2025-07-01"
    assert data["end_date"] == "2025-07-31"

def test_ping_endpoint():
    response = client.get("/data/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "data router alive" in data["message"]

def test_ingest_data_endpoint():
    alerts = load_alerts_csv()
    sample = alerts[0]
    payload = {
        "name": sample["Name"],
        "timestamp": sample["Time"],
        "payload": {
            "alert_id": sample["Alert ID"],
            "ticker": sample["Ticker"],
            "description": sample["Description"]
        }
    }
    response = client.post("/data/ingest", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["received"] is True
    assert data["name"] == sample["Name"]
    assert data["timestamp"] == sample["Time"]

def test_list_items_endpoint():
    response = client.get("/data/items?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "items" in data
    assert data["limit"] == 5

def test_normalize_filters_invalid_time():
    payload = {
        "start_time": "25:00",  # invalid hour
        "end_time": "16:00"
    }
    response = client.post("/data/filters/normalize", json=payload)
    assert response.status_code == 422
    assert "time must be in HH:MM format" in response.text or "hour must be 0..23" in response.text

def test_normalize_filters_missing_end_time():
    payload = {
        "start_time": "09:00"
    }
    response = client.post("/data/filters/normalize", json=payload)
    assert response.status_code == 422
    assert "Both start_time and end_time must be provided together" in response.text
