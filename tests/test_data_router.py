import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from routes.data.router import data_router
from routes.data.schemas import AlertCreate, AlertRead, AlertUpdate

@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(data_router)
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

@pytest.mark.asyncio
async def test_list_data(client, monkeypatch):
    mock_service = AsyncMock()
    mock_service.list.return_value = [AlertRead(id="507f1f77bcf86cd799439011", contract="NQ1!", trade_type="buy", quantity=1, price=100.0, secret_key=None, timestamp=None)]
    monkeypatch.setattr("routes.data.router.get_service", lambda: mock_service)
    response = client.get("/data/")
    assert response.status_code == 200
    assert response.json()[0]["id"] == "507f1f77bcf86cd799439011"

@pytest.mark.asyncio
async def test_get_data_found(client, monkeypatch):
    mock_service = AsyncMock()
    mock_service.get.return_value = AlertRead(id="507f1f77bcf86cd799439011", contract="NQ1!", trade_type="buy", quantity=1, price=100.0, secret_key=None, timestamp=None)
    monkeypatch.setattr("routes.data.router.get_service", lambda: mock_service)
    response = client.get("/data/507f1f77bcf86cd799439011")
    assert response.status_code == 200
    assert response.json()["id"] == "507f1f77bcf86cd799439011"

@pytest.mark.asyncio
async def test_get_data_not_found(client, monkeypatch):
    mock_service = AsyncMock()
    mock_service.get.return_value = None
    monkeypatch.setattr("routes.data.router.get_service", lambda: mock_service)
    response = client.get("/data/badid")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_data(client, monkeypatch):
    mock_service = AsyncMock()
    payload = {"contract": "NQ1!", "trade_type": "buy", "quantity": 1, "price": 100.0}
    mock_service.create.return_value = AlertRead(id="507f1f77bcf86cd799439011", **payload)
    monkeypatch.setattr("routes.data.router.get_service", lambda: mock_service)
    response = client.post("/data/", json=payload)
    assert response.status_code == 201
    assert response.json()["id"] == "507f1f77bcf86cd799439011"

@pytest.mark.asyncio
async def test_update_data(client, monkeypatch):
    mock_service = AsyncMock()
    payload = {"quantity": 2}
    mock_service.update.return_value = AlertRead(id="507f1f77bcf86cd799439011", contract="NQ1!", trade_type="buy", quantity=2, price=100.0, secret_key=None, timestamp=None)
    monkeypatch.setattr("routes.data.router.get_service", lambda: mock_service)
    response = client.put("/data/507f1f77bcf86cd799439011", json=payload)
    assert response.status_code == 200
    assert response.json()["quantity"] == 2

@pytest.mark.asyncio
async def test_delete_data(client, monkeypatch):
    mock_service = AsyncMock()
    mock_service.delete.return_value = True
    monkeypatch.setattr("routes.data.router.get_service", lambda: mock_service)
    response = client.delete("/data/507f1f77bcf86cd799439011")
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_delete_data_not_found(client, monkeypatch):
    mock_service = AsyncMock()
    mock_service.delete.return_value = False
    monkeypatch.setattr("routes.data.router.get_service", lambda: mock_service)
    response = client.delete("/data/badid")
    assert response.status_code == 404

