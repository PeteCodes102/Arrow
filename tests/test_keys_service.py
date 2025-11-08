"""Tests for routes/keys/service.py"""
import pytest
from unittest.mock import AsyncMock, patch
from routes.keys.service import KeysService
from routes.keys.schemas import KeysCreate, KeysRead, KeysUpdate


@pytest.mark.asyncio
async def test_keys_service_create_generates_key_if_not_provided():
    """Test that service generates a secret key if not provided."""
    repo = AsyncMock()
    service = KeysService(repo)
    
    payload = KeysCreate(name="Test Strategy", secret_key=None)
    expected_read = KeysRead(
        id="507f1f77bcf86cd799439011",
        secret_key="generated_key_123",
        name="Test Strategy"
    )
    repo.create.return_value = expected_read
    
    result = await service.create(payload)
    
    # Verify secret_key was set before calling repo.create
    assert payload.secret_key is not None
    assert len(payload.secret_key) > 0
    repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_keys_service_create_uses_provided_key():
    """Test that service uses provided secret key."""
    repo = AsyncMock()
    service = KeysService(repo)
    
    provided_key = "my_custom_secret_key"
    payload = KeysCreate(name="Test Strategy", secret_key=provided_key)
    expected_read = KeysRead(
        id="507f1f77bcf86cd799439011",
        secret_key=provided_key,
        name="Test Strategy"
    )
    repo.create.return_value = expected_read
    
    result = await service.create(payload)
    
    assert result.secret_key == provided_key
    assert payload.secret_key == provided_key


@pytest.mark.asyncio
async def test_keys_service_get_name_by_key_found():
    """Test successful lookup of strategy name by secret key."""
    repo = AsyncMock()
    service = KeysService(repo)
    
    secret_key = "test_key_123"
    expected_read = KeysRead(
        id="507f1f77bcf86cd799439011",
        secret_key=secret_key,
        name="My Strategy"
    )
    repo.get_by_secret_key.return_value = expected_read
    
    result = await service.get_name_by_key(secret_key)
    
    assert result == "My Strategy"
    repo.get_by_secret_key.assert_called_once_with(secret_key)


@pytest.mark.asyncio
async def test_keys_service_get_name_by_key_not_found():
    """Test lookup with invalid secret key returns None."""
    repo = AsyncMock()
    service = KeysService(repo)
    
    repo.get_by_secret_key.return_value = None
    
    result = await service.get_name_by_key("invalid_key")
    
    assert result is None


@pytest.mark.asyncio
async def test_keys_service_list():
    """Test listing all keys."""
    repo = AsyncMock()
    service = KeysService(repo)
    
    expected_keys = [
        KeysRead(id="507f1f77bcf86cd799439011", secret_key="key1", name="Strategy 1"),
        KeysRead(id="507f1f77bcf86cd799439012", secret_key="key2", name="Strategy 2"),
    ]
    repo.list.return_value = expected_keys
    
    result = await service.list()
    
    assert len(result) == 2
    assert result == expected_keys


@pytest.mark.asyncio
async def test_keys_service_get():
    """Test getting a specific key by ID."""
    repo = AsyncMock()
    service = KeysService(repo)
    
    item_id = "507f1f77bcf86cd799439011"
    expected_read = KeysRead(id=item_id, secret_key="key1", name="Strategy 1")
    repo.get.return_value = expected_read
    
    result = await service.get(item_id)
    
    assert result == expected_read
    repo.get.assert_called_once_with(item_id)


@pytest.mark.asyncio
async def test_keys_service_update():
    """Test updating a key entry."""
    repo = AsyncMock()
    service = KeysService(repo)
    
    item_id = "507f1f77bcf86cd799439011"
    update_payload = KeysUpdate(name="Updated Strategy")
    expected_read = KeysRead(id=item_id, secret_key="key1", name="Updated Strategy")
    repo.update.return_value = expected_read
    
    result = await service.update(item_id, update_payload)
    
    assert result.name == "Updated Strategy"
    repo.update.assert_called_once_with(item_id, update_payload)


@pytest.mark.asyncio
async def test_keys_service_delete():
    """Test deleting a key entry."""
    repo = AsyncMock()
    service = KeysService(repo)
    
    item_id = "507f1f77bcf86cd799439011"
    repo.delete.return_value = True
    
    result = await service.delete(item_id)
    
    assert result is True
    repo.delete.assert_called_once_with(item_id)
