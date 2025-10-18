import pytest
from routes.data.schemas import AlertQuery, AlertRead
from routes.data.service import DataService
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_query_by_user_id_and_strategy(monkeypatch):
    # Mock DataService and its repo.query method
    service = DataService(repo=AsyncMock())
    expected = [AlertRead(id="1", contract="NQ1!", trade_type="buy", quantity=1, price=100.0, secret_key=None, timestamp=None)]
    service.repo.query = AsyncMock(return_value=expected)
    query = AlertQuery(user_id="user123", strategy_name="stratA")
    result = await service.query(query)
    assert result == expected

@pytest.mark.asyncio
async def test_query_with_options(monkeypatch):
    service = DataService(repo=AsyncMock())
    expected = [AlertRead(id="2", contract="NQ1!", trade_type="sell", quantity=2, price=200.0, secret_key=None, timestamp=None)]
    service.repo.query = AsyncMock(return_value=expected)
    query = AlertQuery(options={"trade_type": "sell", "quantity": 2})
    result = await service.query(query)
    assert result == expected

@pytest.mark.asyncio
async def test_query_empty(monkeypatch):
    service = DataService(repo=AsyncMock())
    service.repo.query = AsyncMock(return_value=[])
    query = AlertQuery()
    result = await service.query(query)
    assert result == []

