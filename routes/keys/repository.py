from typing import List, Optional
from itertools import count
from .schemas import KeysCreate, KeysRead, KeysUpdate
from models.secret_key import SecretKeyIndex

class KeysRepository:
    """
    Data access layer for keys.
    This in-memory implementation is for development; replace with a database-backed repo.
    """

    async def list(self) -> List[KeysRead]:
        docs = await SecretKeyIndex.find_all().to_list()
        return [
            KeysRead(
                id=str(doc.id),
                **doc.model_dump(by_alias=True, exclude={'id'}),
            )
            for doc in docs
        ]

    async def get(self, item_id: str) -> Optional[KeysRead]:
        doc = await SecretKeyIndex.get(item_id)
        if not doc:
            return None
        return KeysRead(id=str(doc.id), **doc.model_dump(by_alias=True, exclude={'id'}))

    async def create(self, payload: KeysCreate) -> KeysRead:
        doc = SecretKeyIndex(**payload.model_dump())
        await doc.insert()
        return KeysRead(id=str(doc.id), **doc.model_dump(by_alias=True, exclude={'id'}))

    async def update(self, item_id: str, payload: KeysUpdate) -> Optional[KeysRead]:
        doc = await SecretKeyIndex.get(item_id)
        if not doc:
            return None
        update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
        for k, v in update_data.items():
            setattr(doc, k, v)
        await doc.save()
        return KeysRead(id=str(doc.id), **doc.model_dump(by_alias=True, exclude={'id'}))

    async def search(self, first: bool = False, **kwargs):
        query = SecretKeyIndex.find_many(kwargs)
        if first:
            doc = await query.first_or_none()
            if doc:
                return KeysRead(id=str(doc.id), **doc.model_dump(by_alias=True, exclude={'id'}))
            return None
        docs = await query.to_list()
        return [
            KeysRead(
                id=str(doc.id),
                **doc.model_dump(by_alias=True, exclude={'id'}),
            )
            for doc in docs
        ]

    async def delete(self, item_id: str) -> bool:
        doc = await SecretKeyIndex.get(item_id)
        if not doc:
            return False
        await doc.delete()
        return True

