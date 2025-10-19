from typing import List, Optional
from models.alerts import BaseAlert
from .schemas import AlertCreate, AlertRead, AlertUpdate, AlertQuery

class DataRepository:
    """
    Data access layer for data using Beanie ODM (MongoDB).
    """
    async def list(self) -> List[AlertRead]:
        docs = await BaseAlert.find_all().to_list()
        return [
            AlertRead(
                id=str(doc.id),
                **doc.model_dump(by_alias=True, exclude={'id'}),
            )
            for doc in docs
        ]

    async def get(self, item_id: str) -> Optional[AlertRead]:
        doc = await BaseAlert.get(item_id)
        if doc:
            return AlertRead(
                id=str(doc.id),
                **doc.model_dump(by_alias=True, exclude={'id'}),
            )
        return None

    async def create(self, payload: AlertCreate) -> AlertRead:
        doc = BaseAlert(**payload.model_dump(by_alias=True))
        await doc.insert()
        return AlertRead(
            id=str(doc.id),
            **doc.model_dump(by_alias=True, exclude={'id'}),
        )

    async def update(self, item_id: str, payload: AlertUpdate) -> Optional[AlertRead]:
        doc = await BaseAlert.get(item_id)
        if not doc:
            return None
        update_data = payload.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(doc, k, v)
        await doc.save()
        return AlertRead(
            id=str(doc.id),
            **doc.model_dump(by_alias=True, exclude={'id'}),
        )

    async def delete(self, item_id: str) -> bool:
        doc = await BaseAlert.get(item_id)
        if doc:
            await doc.delete()
            return True
        return False

    async def query(self, query: AlertQuery) -> List[AlertRead]:
        filter_dict = {}
        if query.user_id:
            filter_dict['userId'] = query.user_id
        if query.strategy_name:
            filter_dict['strategy'] = query.strategy_name
        if query.options:
            filter_dict.update(query.options)
        docs = await BaseAlert.find(filter_dict).to_list()
        return [
            AlertRead(
                id=str(doc.id),
                **doc.model_dump(by_alias=True, exclude={'id'}),
            )
            for doc in docs
        ]
