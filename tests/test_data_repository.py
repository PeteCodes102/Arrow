import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from routes.data.repository import DataRepository, DataDocument
from routes.data.schemas import AlertCreate, DataUpdate

@pytest.mark.asyncio
async def test_create_and_get():
    repo = DataRepository()
    payload = AlertCreate(contract="NQ1!", trade_type="buy", quantity=1, price=100.0)
    with patch.object(DataDocument, "insert", new_callable=AsyncMock) as mock_insert, \
         patch.object(DataDocument, "get", new_callable=AsyncMock) as mock_get:
        doc = DataDocument(**payload.model_dump())
        doc.id = "507f1f77bcf86cd799439011"
        mock_insert.return_value = None
        mock_get.return_value = doc
        created = await repo.create(payload)
        assert created.id == "507f1f77bcf86cd799439011"
        fetched = await repo.get("507f1f77bcf86cd799439011")
        assert fetched.id == "507f1f77bcf86cd799439011"

@pytest.mark.asyncio
async def test_update_and_delete():
    repo = DataRepository()
    payload = AlertCreate(contract="NQ1!", trade_type="buy", quantity=1, price=100.0)
    update = DataUpdate(quantity=5)
    with patch.object(DataDocument, "get", new_callable=AsyncMock) as mock_get, \
         patch.object(DataDocument, "save", new_callable=AsyncMock) as mock_save, \
         patch.object(DataDocument, "delete", new_callable=AsyncMock) as mock_delete:
        doc = DataDocument(**payload.model_dump())
        doc.id = "507f1f77bcf86cd799439011"
        mock_get.return_value = doc
        mock_save.return_value = None
        mock_delete.return_value = None
        updated = await repo.update("507f1f77bcf86cd799439011", update)
        assert updated.quantity == 5
        deleted = await repo.delete("507f1f77bcf86cd799439011")
        assert deleted is True

@pytest.mark.asyncio
async def test_list():
    repo = DataRepository()
    with patch.object(DataDocument, "find_all", new_callable=AsyncMock) as mock_find_all:
        doc = DataDocument(contract="NQ1!", trade_type="buy", quantity=1, price=100.0)
        doc.id = "507f1f77bcf86cd799439011"
        mock_find_all.return_value.to_list = AsyncMock(return_value=[doc])
        items = await repo.list()
        assert len(items) == 1
        assert items[0].id == "507f1f77bcf86cd799439011"

