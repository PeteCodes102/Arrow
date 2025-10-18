import pytest
from fastapi import Request
from core.deps import get_db, get_service
from unittest.mock import MagicMock, AsyncMock

class DummyRequest:
    def __init__(self, db):
        self.state = MagicMock()
        self.state.db = db

@pytest.mark.asyncio
async def test_get_db_returns_db():
    dummy_db = MagicMock()
    request = DummyRequest(dummy_db)
    result = get_db(request)
    assert result == dummy_db

@pytest.mark.asyncio
async def test_get_service_returns_dataservice():
    service = await get_service()
    assert hasattr(service, 'repo')
