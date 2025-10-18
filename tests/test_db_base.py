import pytest
from unittest.mock import AsyncMock, patch
from db.base import init_db, create_item, get_item, update_item, delete_item, find_items
from models.alerts import BaseAlert

@pytest.mark.asyncio
async def test_init_db_initializes_beanie():
    with patch('db.base.init_beanie', new_callable=AsyncMock) as mock_init:
        await init_db('mongodb://localhost', 'testdb', models=[BaseAlert])
        mock_init.assert_awaited_once()

@pytest.mark.asyncio
async def test_create_get_update_delete_item():
    item = BaseAlert(contract='NQ1!', trade_type='buy', quantity=1, price=100.0)
    with patch.object(item, 'insert', new_callable=AsyncMock) as mock_insert:
        await create_item(item)
        mock_insert.assert_awaited_once()
    with patch.object(BaseAlert, 'get', new_callable=AsyncMock) as mock_get:
        await get_item(BaseAlert, 'some_id')
        mock_get.assert_awaited_once_with('some_id')
    with patch.object(item, 'save', new_callable=AsyncMock) as mock_save:
        await update_item(item, {'price': 200.0})
        assert item.price == 200.0
        mock_save.assert_not_called()  # update_item does not call save in your code
    with patch.object(item, 'delete', new_callable=AsyncMock) as mock_delete:
        await delete_item(item)
        mock_delete.assert_awaited_once()
    with patch.object(BaseAlert, 'find', new_callable=AsyncMock) as mock_find:
        await find_items(BaseAlert, {'trade_type': 'buy'})
        mock_find.assert_awaited_once()
