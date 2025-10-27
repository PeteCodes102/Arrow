from typing import List, Optional
from bson import ObjectId
from .schemas import KeysCreate, KeysRead, KeysUpdate
from models.secret_key import SecretKeyIndex


class KeysRepository:
    """
    Data access layer for secret keys using Beanie ODM.

    This repository handles all database operations for secret key management,
    including CRUD operations and specialized queries.
    """

    async def list(self) -> List[KeysRead]:
        """Retrieve all secret keys."""
        docs = await SecretKeyIndex.find_all().to_list()
        return [
            KeysRead(
                id=str(doc.id),
                **doc.model_dump(by_alias=True, exclude={'id'}),
            )
            for doc in docs
        ]

    async def get(self, item_id: str) -> Optional[KeysRead]:
        """
        Retrieve a secret key by its ID.

        Args:
            item_id: The MongoDB ObjectId as a string

        Returns:
            KeysRead if found, None otherwise
        """
        try:
            doc = await SecretKeyIndex.get(ObjectId(item_id))
        except Exception:
            return None

        if not doc:
            return None
        return KeysRead(id=str(doc.id), **doc.model_dump(by_alias=True, exclude={'id'}))

    async def create(self, payload: KeysCreate) -> KeysRead:
        """
        Create a new secret key entry.

        Args:
            payload: The key creation data

        Returns:
            The created key
        """
        doc = SecretKeyIndex(**payload.model_dump())
        await doc.insert()
        return KeysRead(id=str(doc.id), **doc.model_dump(by_alias=True, exclude={'id'}))

    async def update(self, item_id: str, payload: KeysUpdate) -> Optional[KeysRead]:
        """
        Update an existing secret key entry.

        Args:
            item_id: The MongoDB ObjectId as a string
            payload: The update data

        Returns:
            The updated key if found, None otherwise
        """
        try:
            doc = await SecretKeyIndex.get(ObjectId(item_id))
        except Exception:
            return None

        if not doc:
            return None

        update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
        for k, v in update_data.items():
            setattr(doc, k, v)
        await doc.save()
        return KeysRead(id=str(doc.id), **doc.model_dump(by_alias=True, exclude={'id'}))

    async def delete(self, item_id: str) -> bool:
        """
        Delete a secret key entry.

        Args:
            item_id: The MongoDB ObjectId as a string

        Returns:
            True if deleted, False if not found
        """
        try:
            doc = await SecretKeyIndex.get(ObjectId(item_id))
        except Exception:
            return False

        if not doc:
            return False
        await doc.delete()
        return True

    async def get_by_secret_key(self, secret_key: str) -> Optional[KeysRead]:
        """
        Retrieve a key entry by its secret key (optimized query).

        Args:
            secret_key: The secret key to search for

        Returns:
            KeysRead if found, None otherwise
        """
        doc = await SecretKeyIndex.find_one(SecretKeyIndex.secret_key == secret_key)
        if doc:
            return KeysRead(id=str(doc.id), **doc.model_dump(by_alias=True, exclude={'id'}))
        return None

    async def search_by_name(self, name: str) -> List[KeysRead]:
        """
        Search for keys by strategy name (optimized query).

        Args:
            name: The strategy name to search for

        Returns:
            List of matching keys
        """
        docs = await SecretKeyIndex.find(SecretKeyIndex.name == name).to_list()
        return [
            KeysRead(
                id=str(doc.id),
                **doc.model_dump(by_alias=True, exclude={'id'}),
            )
            for doc in docs
        ]

    async def search(self, first: bool = False, **kwargs) -> Optional[KeysRead] | List[KeysRead]:
        """
        Generic search method for backward compatibility.

        Args:
            first: If True, return only the first result
            **kwargs: Field filters (e.g., secret_key='xyz', name='Strategy A')

        Returns:
            Single KeysRead if first=True, List of KeysRead otherwise
        """
        # Build query filter
        query_filter = {}
        for key, value in kwargs.items():
            if hasattr(SecretKeyIndex, key):
                query_filter[key] = value

        if first:
            doc = await SecretKeyIndex.find_one(query_filter)
            if doc:
                return KeysRead(id=str(doc.id), **doc.model_dump(by_alias=True, exclude={'id'}))
            return None

        docs = await SecretKeyIndex.find(query_filter).to_list()
        return [
            KeysRead(
                id=str(doc.id),
                **doc.model_dump(by_alias=True, exclude={'id'}),
            )
            for doc in docs
        ]


