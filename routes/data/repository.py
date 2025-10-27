from typing import List, Optional
from bson import ObjectId
from models.alerts import BaseAlert
from .schemas import AlertCreate, AlertRead, AlertUpdate, AlertQuery


class DataRepository:
    """
    Data access layer for trading alerts using Beanie ODM (MongoDB).

    This repository handles all database operations for alert management,
    providing optimized queries and proper error handling.
    """

    async def list(self, limit: Optional[int] = None) -> List[AlertRead]:
        """
        Retrieve all alerts with optional limit.

        Args:
            limit: Maximum number of alerts to return (None for all)

        Returns:
            List of alerts
        """
        query = BaseAlert.find_all()
        if limit:
            query = query.limit(limit)
        docs = await query.to_list()
        return [
            AlertRead(
                id=str(doc.id),
                **doc.model_dump(by_alias=True, exclude={'id'}),
            )
            for doc in docs
        ]

    async def get(self, item_id: str) -> Optional[AlertRead]:
        """
        Retrieve a single alert by ID.

        Args:
            item_id: The MongoDB ObjectId as a string

        Returns:
            AlertRead if found, None otherwise
        """
        try:
            doc = await BaseAlert.get(ObjectId(item_id))
        except Exception:
            return None

        if doc:
            return AlertRead(
                id=str(doc.id),
                **doc.model_dump(by_alias=True, exclude={'id'}),
            )
        return None

    async def create(self, payload: AlertCreate) -> AlertRead:
        """
        Create a new alert.

        Args:
            payload: The alert creation data

        Returns:
            The created alert
        """
        doc = BaseAlert(**payload.model_dump(by_alias=True))
        await doc.insert()
        return AlertRead(
            id=str(doc.id),
            **doc.model_dump(by_alias=True, exclude={'id'}),
        )

    async def update(self, item_id: str, payload: AlertUpdate) -> Optional[AlertRead]:
        """
        Update an existing alert.

        Args:
            item_id: The MongoDB ObjectId as a string
            payload: The update data (only non-None fields will be updated)

        Returns:
            The updated alert if found, None otherwise
        """
        try:
            doc = await BaseAlert.get(ObjectId(item_id))
        except Exception:
            return None

        if not doc:
            return None

        update_data = payload.model_dump(exclude_unset=True, by_alias=True)
        for k, v in update_data.items():
            setattr(doc, k, v)
        await doc.save()
        return AlertRead(
            id=str(doc.id),
            **doc.model_dump(by_alias=True, exclude={'id'}),
        )

    async def delete(self, item_id: str) -> bool:
        """
        Delete an alert.

        Args:
            item_id: The MongoDB ObjectId as a string

        Returns:
            True if deleted, False if not found
        """
        try:
            doc = await BaseAlert.get(ObjectId(item_id))
        except Exception:
            return False

        if doc:
            await doc.delete()
            return True
        return False

    async def query(self, query: AlertQuery) -> List[AlertRead]:
        """
        Query alerts with filters.

        Args:
            query: Query parameters including user_id, strategy_name, and options

        Returns:
            List of matching alerts
        """
        filter_conditions = []

        if query.user_id:
            filter_conditions.append(BaseAlert.userId == query.user_id)
        if query.strategy_name:
            filter_conditions.append(BaseAlert.name == query.strategy_name)
        if query.options:
            for key, value in query.options.items():
                if hasattr(BaseAlert, key):
                    filter_conditions.append(getattr(BaseAlert, key) == value)

        if filter_conditions:
            # Combine conditions with AND logic
            docs = await BaseAlert.find(*filter_conditions).to_list()
        else:
            docs = await BaseAlert.find_all().to_list()

        return [
            AlertRead(
                id=str(doc.id),
                **doc.model_dump(by_alias=True, exclude={'id'}),
            )
            for doc in docs
        ]
