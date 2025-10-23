from typing import List, Optional
from itertools import count
from .schemas import KeysCreate, KeysRead, KeysUpdate

class KeysRepository:
    """
    Data access layer for keys.
    This in-memory implementation is for development; replace with a database-backed repo.
    """
    _ids = count(1)

    def __init__(self):
        self._items: dict[int, KeysRead] = {}

    def list(self) -> List[KeysRead]:
        return list(self._items.values())

    def get(self, item_id: int) -> Optional[KeysRead]:
        return self._items.get(item_id)

    def create(self, payload: KeysCreate) -> KeysRead:
        new_id = next(self._ids)
        item = KeysRead(id=new_id, **payload.model_dump())
        self._items[new_id] = item
        return item

    def update(self, item_id: int, payload: KeysUpdate) -> Optional[KeysRead]:
        existing = self._items.get(item_id)
        if not existing:
            return None
        data = existing.model_dump()
        data.update({Settings: v for Settings, v in payload.model_dump().items() if v is not None})
        updated = KeysRead(**data)
        self._items[item_id] = updated
        return updated

    def delete(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None
