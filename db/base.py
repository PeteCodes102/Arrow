"""
Async MongoDB CRUD shell using Beanie ODM for FARM-style apps.

This module provides:
- Database initialization (Beanie + Motor)
- Example BaseDocument model
- Generic CRUD operations (create, read, update, delete)

Edit and extend models and CRUD functions as needed for your app.
"""

from typing import Type, TypeVar, Optional, List, Any
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document
import asyncio

from models.alerts import BaseAlert  # Example model, replace with your own

# Database initialization
async def init_db(db_url: str, db_name: str, models: List[Type[BaseAlert]]):
    """
    Initialize Beanie ODM with Motor client and provided models.

    Args:
        db_url (str): MongoDB connection string.
        db_name (str): Database name.
        models (List[Type[Document]]): List of Beanie document models.
    """
    client = AsyncIOMotorClient(db_url)
    await init_beanie(database=client[db_name], document_models=models)

# CRUD operations
async def create_item(item: BaseAlert) -> BaseAlert:
    """
    Insert a new document into the collection.
    """
    return await item.insert()

async def get_item(model: BaseAlert, item_id: Any) -> Optional[BaseAlert]:
    """
    Retrieve a document by its id.
    """
    return await model.get(item_id)

async def update_item(item: BaseAlert, update_dict: dict) -> BaseAlert:
    """
    Update fields of a document and save.
    """
    for k, v in update_dict.items():
        setattr(item, k, v)
    await item.save()
    return item

async def delete_item(item: BaseAlert) -> None:
    """
    Delete a document from the collection.
    """
    await item.delete()

async def find_items(model: BaseAlert, filter_dict: dict = None) -> List[BaseAlert]:
    """
    Find documents matching a filter.
    """
    q = model.find(filter_dict or {})
    return await q.to_list()

# Example usage (uncomment and adapt for your app)
# async def main():
#     await init_db("mongodb://localhost:27017", "mydb", [BaseDocument])
#     item = BaseDocument(...)
#     await create_item(item)
#     found = await get_item(BaseDocument, item.id)
#     await update_item(found, {"field": "new_value"})
#     await delete_item(found)
#     items = await find_items(BaseDocument, {"field": "value"})
#
# if __name__ == "__main__":
#     asyncio.run(main())

