"""Tests for routes/router.py - Alert router with strategy-based operations"""
import pytest
from unittest.mock import AsyncMock, patch, create_autospec
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.router import alert_router, get_service_worker
from routes.data.schemas import AlertCreate, AlertRead
from routes.keys.schemas import KeysRead
from routes.services import ServiceWorker
from routes.data.service import DataService
from routes.keys.service import KeysService


@pytest.fixture
def app():
    """Create a FastAPI app with the alert router."""
    app = FastAPI()
    app.include_router(alert_router)
    return app


@pytest.fixture
def client(app):
    """Create a test client."""
    return TestClient(app)


def test_get_strategy_names(client):
    """Test getting all strategy names."""
    # Create mock worker
    keys_service = create_autospec(KeysService, instance=True)
    data_service = create_autospec(DataService, instance=True)
    data_service.get_strategy_names = AsyncMock(return_value=["Strategy 1", "Strategy 2"])
    
    mock_worker = ServiceWorker(keys_service=keys_service, data_service=data_service)
    
    async def override_get_service_worker():
        return mock_worker
    
    # Override the dependency
    client.app.dependency_overrides[get_service_worker] = override_get_service_worker
    
    response = client.get("/alerts/strategy_names")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert "Strategy 1" in data
    assert "Strategy 2" in data


def test_create_alert_with_secret_key(client):
    """Test creating an alert with a valid secret key."""
    # Create mock services
    keys_service = create_autospec(KeysService, instance=True)
    data_service = create_autospec(DataService, instance=True)
    
    keys_service.get_name_by_key = AsyncMock(return_value="Test Strategy")
    
    payload = {
        "contract": "NQ1!",
        "trade_type": "buy",
        "quantity": 1,
        "price": 100.0
    }
    
    expected_alert = AlertRead(
        id="507f1f77bcf86cd799439011",
        contract="NQ1!",
        trade_type="buy",
        quantity=1,
        price=100.0,
        name="Test Strategy",
        secret_key="test_key_123"
    )
    
    data_service.create = AsyncMock(return_value=expected_alert)
    
    mock_worker = ServiceWorker(keys_service=keys_service, data_service=data_service)
    
    async def override_get_service_worker():
        return mock_worker
    
    client.app.dependency_overrides[get_service_worker] = override_get_service_worker
    
    response = client.post("/alerts/create/test_key_123", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Strategy"
    assert data["contract"] == "NQ1!"


def test_create_alert_with_invalid_key(client):
    """Test creating an alert with an invalid secret key."""
    from fastapi import HTTPException
    
    # Create mock services
    keys_service = create_autospec(KeysService, instance=True)
    data_service = create_autospec(DataService, instance=True)
    
    keys_service.get_name_by_key = AsyncMock(return_value=None)
    
    mock_worker = ServiceWorker(keys_service=keys_service, data_service=data_service)
    
    async def override_get_service_worker():
        return mock_worker
    
    client.app.dependency_overrides[get_service_worker] = override_get_service_worker
    
    payload = {
        "contract": "NQ1!",
        "trade_type": "buy",
        "quantity": 1,
        "price": 100.0
    }
    
    response = client.post("/alerts/create/invalid_key", json=payload)
    
    assert response.status_code == 401


def test_bind_key_to_name_success(client):
    """Test binding a new secret key to a strategy name."""
    # Create mock services
    keys_service = create_autospec(KeysService, instance=True)
    keys_service.repo = AsyncMock()
    data_service = create_autospec(DataService, instance=True)
    
    keys_service.repo.search_by_name = AsyncMock(return_value=[])
    
    expected_key = KeysRead(
        id="507f1f77bcf86cd799439011",
        secret_key="new_generated_key_abc123",
        name="My New Strategy"
    )
    
    keys_service.create = AsyncMock(return_value=expected_key)
    
    mock_worker = ServiceWorker(keys_service=keys_service, data_service=data_service)
    
    async def override_get_service_worker():
        return mock_worker
    
    client.app.dependency_overrides[get_service_worker] = override_get_service_worker
    
    payload = {"name": "My New Strategy"}
    response = client.post("/alerts/bind_key", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My New Strategy"
    assert "secret_key" in data
    assert len(data["secret_key"]) > 0


def test_bind_key_to_existing_name_conflict(client):
    """Test binding a key to a name that already has one."""
    from fastapi import HTTPException
    
    # Create mock services
    keys_service = create_autospec(KeysService, instance=True)
    keys_service.repo = AsyncMock()
    data_service = create_autospec(DataService, instance=True)
    
    existing_key = KeysRead(
        id="507f1f77bcf86cd799439011",
        secret_key="existing_key",
        name="Existing Strategy"
    )
    keys_service.repo.search_by_name = AsyncMock(return_value=[existing_key])
    
    mock_worker = ServiceWorker(keys_service=keys_service, data_service=data_service)
    
    async def override_get_service_worker():
        return mock_worker
    
    client.app.dependency_overrides[get_service_worker] = override_get_service_worker
    
    payload = {"name": "Existing Strategy"}
    response = client.post("/alerts/bind_key", json=payload)
    
    assert response.status_code == 409
    assert "already bound" in response.json()["detail"]
