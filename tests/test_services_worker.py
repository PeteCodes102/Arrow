"""Tests for routes/services.py - ServiceWorker orchestration layer"""
import pytest
from unittest.mock import AsyncMock, MagicMock, create_autospec
from fastapi import HTTPException
from routes.services import ServiceWorker
from routes.data.schemas import AlertCreate, AlertRead
from routes.data.service import DataService
from routes.keys.schemas import KeysCreate, KeysRead
from routes.keys.service import KeysService


@pytest.mark.asyncio
async def test_service_worker_create_alert_success():
    """Test successful alert creation with valid secret key."""
    # Create mock services using create_autospec to pass type validation
    keys_service = create_autospec(KeysService, instance=True)
    data_service = create_autospec(DataService, instance=True)
    
    # Configure async methods
    keys_service.get_name_by_key = AsyncMock(return_value="Test Strategy")
    
    payload = AlertCreate(
        contract="NQ1!",
        trade_type="buy",
        quantity=1,
        price=100.0
    )
    
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
    
    # Create service worker
    worker = ServiceWorker(
        keys_service=keys_service,
        data_service=data_service
    )
    
    # Execute
    result = await worker.create_alert(payload, "test_key_123")
    
    # Verify
    assert result.name == "Test Strategy"
    assert result.secret_key == "test_key_123"
    keys_service.get_name_by_key.assert_called_once_with("test_key_123")
    data_service.create.assert_called_once()


@pytest.mark.asyncio
async def test_service_worker_create_alert_invalid_key():
    """Test alert creation with invalid secret key raises HTTPException."""
    # Create mock services
    keys_service = create_autospec(KeysService, instance=True)
    data_service = create_autospec(DataService, instance=True)
    
    keys_service.get_name_by_key = AsyncMock(return_value=None)
    data_service.create = AsyncMock()
    
    payload = AlertCreate(
        contract="NQ1!",
        trade_type="buy",
        quantity=1,
        price=100.0
    )
    
    # Create service worker
    worker = ServiceWorker(
        keys_service=keys_service,
        data_service=data_service
    )
    
    # Execute and verify exception
    with pytest.raises(HTTPException) as exc_info:
        await worker.create_alert(payload, "invalid_key")
    
    assert exc_info.value.status_code == 401
    assert "Invalid secret key" in exc_info.value.detail
    data_service.create.assert_not_called()


@pytest.mark.asyncio
async def test_service_worker_bind_key_to_name_success():
    """Test successful binding of new secret key to strategy name."""
    # Create mock services
    keys_service = create_autospec(KeysService, instance=True)
    keys_service.repo = AsyncMock()
    data_service = create_autospec(DataService, instance=True)
    
    # No existing keys for this name
    keys_service.repo.search_by_name = AsyncMock(return_value=[])
    
    expected_key = KeysRead(
        id="507f1f77bcf86cd799439011",
        secret_key="generated_key_abc123",
        name="New Strategy"
    )
    keys_service.create = AsyncMock(return_value=expected_key)
    
    # Create service worker
    worker = ServiceWorker(
        keys_service=keys_service,
        data_service=data_service
    )
    
    # Execute
    result = await worker.bind_key_to_name("New Strategy")
    
    # Verify
    assert result.name == "New Strategy"
    assert result.secret_key is not None
    keys_service.repo.search_by_name.assert_called_once_with("New Strategy")
    keys_service.create.assert_called_once()


@pytest.mark.asyncio
async def test_service_worker_bind_key_to_name_already_exists():
    """Test binding key to name that already has a key raises HTTPException."""
    # Create mock services
    keys_service = create_autospec(KeysService, instance=True)
    keys_service.repo = AsyncMock()
    data_service = create_autospec(DataService, instance=True)
    
    # Existing key found
    existing_key = KeysRead(
        id="507f1f77bcf86cd799439011",
        secret_key="existing_key",
        name="Existing Strategy"
    )
    keys_service.repo.search_by_name = AsyncMock(return_value=[existing_key])
    keys_service.create = AsyncMock()
    
    # Create service worker
    worker = ServiceWorker(
        keys_service=keys_service,
        data_service=data_service
    )
    
    # Execute and verify exception
    with pytest.raises(HTTPException) as exc_info:
        await worker.bind_key_to_name("Existing Strategy")
    
    assert exc_info.value.status_code == 409
    assert "already bound" in exc_info.value.detail
    keys_service.create.assert_not_called()


@pytest.mark.asyncio
async def test_service_worker_get_strategy_names():
    """Test getting all strategy names."""
    # Create mock services
    keys_service = create_autospec(KeysService, instance=True)
    data_service = create_autospec(DataService, instance=True)
    
    expected_names = ["Strategy 1", "Strategy 2", "Strategy 3"]
    data_service.get_strategy_names = AsyncMock(return_value=expected_names)
    
    # Create service worker
    worker = ServiceWorker(
        keys_service=keys_service,
        data_service=data_service
    )
    
    # Execute
    result = await worker.get_strategy_names()
    
    # Verify
    assert result == expected_names
    assert len(result) == 3
    data_service.get_strategy_names.assert_called_once()
