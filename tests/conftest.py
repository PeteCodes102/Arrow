"""
Shared pytest fixtures for Arrow backend tests.

This module provides common fixtures used across multiple test files,
including mock services, test data, and database setup.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from typing import List
from datetime import datetime, timezone
import os

# Set test environment variables
os.environ.setdefault('MONGO_DB_CONNECTION_STRING', 'mongodb://localhost:27017')
os.environ.setdefault('MONGO_DB_NAME', 'arrow_test')
os.environ.setdefault('ENVIRONMENT', 'testing')
os.environ.setdefault('ALLOWED_ORIGINS', 'http://localhost:3000')

from routes.data.schemas import AlertCreate, AlertRead, AlertUpdate
from routes.keys.schemas import KeysCreate, KeysRead


@pytest.fixture
def sample_alert_create() -> AlertCreate:
    """Sample AlertCreate payload for testing."""
    return AlertCreate(
        contract="NQ1!",
        trade_type="buy",
        quantity=1,
        price=100.0,
        timestamp=datetime.now(timezone.utc),
        name="Test Strategy"
    )


@pytest.fixture
def sample_alert_read() -> AlertRead:
    """Sample AlertRead response for testing."""
    return AlertRead(
        id="507f1f77bcf86cd799439011",
        contract="NQ1!",
        trade_type="buy",
        quantity=1,
        price=100.0,
        timestamp=datetime.now(timezone.utc),
        name="Test Strategy"
    )


@pytest.fixture
def sample_alert_list() -> List[AlertRead]:
    """Sample list of AlertRead objects for testing."""
    return [
        AlertRead(
            id="507f1f77bcf86cd799439011",
            contract="NQ1!",
            trade_type="buy",
            quantity=1,
            price=100.0,
            name="Strategy 1"
        ),
        AlertRead(
            id="507f1f77bcf86cd799439012",
            contract="ES1!",
            trade_type="sell",
            quantity=2,
            price=200.0,
            name="Strategy 2"
        ),
    ]


@pytest.fixture
def sample_alert_update() -> AlertUpdate:
    """Sample AlertUpdate payload for testing."""
    return AlertUpdate(quantity=2, price=150.0)


@pytest.fixture
def mock_data_repository():
    """Mock DataRepository for testing services."""
    return AsyncMock()


@pytest.fixture
def mock_keys_repository():
    """Mock KeysRepository for testing services."""
    return AsyncMock()


@pytest.fixture
def sample_secret_key() -> str:
    """Sample secret key for testing."""
    return "test_secret_key_1234567890abcdef"


@pytest.fixture
def sample_keys_read() -> KeysRead:
    """Sample KeysRead response for testing."""
    return KeysRead(
        secret_key="test_secret_key_1234567890abcdef",
        name="Test Strategy"
    )


@pytest.fixture
def mock_db():
    """Mock database for testing."""
    return MagicMock()


@pytest.fixture
def mock_request():
    """Mock FastAPI request for dependency injection testing."""
    request = MagicMock()
    request.app.state.db = MagicMock()
    return request
