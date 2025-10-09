from typing import List, Optional
from beanie import Document
from .schemas import AlertCreate, AlertRead, AlertUpdate

class DataDocument(Document):
    contract: str
    trade_type: str
    quantity: int
    price: float
    secret_key: Optional[str]
    timestamp: Optional[str]

    class Settings:
        name = "data"

class DataRepository:
    """
    Data access layer for data using Beanie ODM (MongoDB).
    """
    async def list(self) -> List[AlertRead]:
        docs = await DataDocument.find_all().to_list()
        return [AlertRead(id=str(doc.id), **doc.model_dump(exclude={'id'})) for doc in docs]

    async def get(self, item_id: str) -> Optional[AlertRead]:
        doc = await DataDocument.get(item_id)
        if doc:
            return AlertRead(id=str(doc.id), **doc.model_dump(exclude={'id'}))
        return None

    async def create(self, payload: AlertCreate) -> AlertRead:
        doc = DataDocument(**payload.model_dump())
        await doc.insert()
        return AlertRead(id=str(doc.id), **doc.model_dump(exclude={'id'}))

    async def update(self, item_id: str, payload: AlertUpdate) -> Optional[AlertRead]:
        doc = await DataDocument.get(item_id)
        if not doc:
            return None
        update_data = payload.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(doc, k, v)
        await doc.save()
        return AlertRead(id=str(doc.id), **doc.model_dump(exclude={'id'}))

    async def delete(self, item_id: str) -> bool:
        doc = await DataDocument.get(item_id)
        if doc:
            await doc.delete()
            return True
        return False
