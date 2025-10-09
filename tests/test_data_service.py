import pytest
from unittest.mock import AsyncMock
from routes.data.service import DataService
from routes.data.schemas import AlertCreate, DataUpdate, AlertRead

@pytest.mark.asyncio
async def test_service_crud():
    repo = AsyncMock()
    service = DataService(repo)
    payload = AlertCreate(contract="NQ1!", trade_type="buy", quantity=1, price=100.0)
    data_read = AlertRead(id="507f1f77bcf86cd799439011", **payload.model_dump())
    repo.create.return_value = data_read
    repo.get.return_value = data_read
    repo.list.return_value = [data_read]
    repo.update.return_value = data_read
    repo.delete.return_value = True

    created = await service.create(payload)
    assert created.id == "507f1f77bcf86cd799439011"
    fetched = await service.get("507f1f77bcf86cd799439011")
    assert fetched.id == "507f1f77bcf86cd799439011"
    items = await service.list()
    assert len(items) == 1
    updated = await service.update("507f1f77bcf86cd799439011", DataUpdate(quantity=2))
    assert updated.id == "507f1f77bcf86cd799439011"
    deleted = await service.delete("507f1f77bcf86cd799439011")
    assert deleted is True

@pytest.mark.asyncio
async def test_service_not_found():
    repo = AsyncMock()
    service = DataService(repo)
    repo.get.return_value = None
    repo.update.return_value = None
    repo.delete.return_value = False
    assert await service.get("badid") is None
    assert await service.update("badid", DataUpdate(quantity=2)) is None
    assert await service.delete("badid") is False

