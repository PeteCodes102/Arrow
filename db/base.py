"""
Async MongoDB CRUD shell using Beanie ODM for FARM-style apps.

This module provides:
- Database initialization (Beanie + Motor)
- Generic CRUD operations (create, read, update, delete)

Edit and extend models and CRUD functions as needed for your app.
"""

from typing import Type, TypeVar, Optional, List, Any
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=Document)


async def init_db(db_url: str, db_name: str, models: List[Type[Document]]) -> AsyncIOMotorClient:
    """
    Initialize Beanie ODM with Motor client and provided models.

    Args:
        db_url (str): MongoDB connection string.
        db_name (str): Database name.
        models (List[Type[Document]]): List of Beanie document models.

    Returns:
        AsyncIOMotorClient: The MongoDB client instance

    Raises:
        Exception: If database initialization fails
    """
    try:
        client = AsyncIOMotorClient(db_url)
        await init_beanie(database=client[db_name], document_models=models)
        logger.info(f"Database '{db_name}' initialized with {len(models)} models")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


# Generic CRUD operations

async def create_item(item: T) -> T:
    """
    Insert a new document into the collection.

    Args:
        item: The document to insert

    Returns:
        The inserted document with ID
    """
    return await item.insert()


async def get_item(model: Type[T], item_id: Any) -> Optional[T]:
    """
    Retrieve a document by its id.

    Args:
        model: The document model class
        item_id: The document ID

    Returns:
        The document if found, None otherwise
    """
    return await model.get(item_id)


async def update_item(item: T, update_dict: dict) -> T:
    """
    Update fields of a document and save.

    Args:
        item: The document to update
        update_dict: Dictionary of field updates

    Returns:
        The updated document
    """
    for k, v in update_dict.items():
        setattr(item, k, v)
    await item.save()
    return item


async def delete_item(item: T) -> None:
    """
    Delete a document from the collection.

    Args:
        item: The document to delete
    """
    await item.delete()


async def find_items(model: Type[T], filter_dict: dict = None) -> List[T]:
    """
    Find documents matching a filter.

    Args:
        model: The document model class
        filter_dict: Filter criteria (None for all documents)

    Returns:
        List of matching documents
    """
    q = model.find(filter_dict or {})
    return await q.to_list()


