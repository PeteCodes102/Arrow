from typing import List, Optional
from .schemas import KeysCreate, KeysRead, KeysUpdate
from .repository import KeysRepository

class KeysService:
    """
    Business logic layer for keys.
    """
    def __init__(self, repo: KeysRepository):
        self.repo = repo

    def list(self) -> List[KeysRead]:
        return self.repo.list()

    def get(self, item_id: int) -> Optional[KeysRead]:
        return self.repo.get(item_id)

    def create(self, payload: KeysCreate) -> KeysRead:
        return self.repo.create(payload)

    def update(self, item_id: int, payload: KeysUpdate) -> Optional[KeysRead]:
        return self.repo.update(item_id, payload)

    def delete(self, item_id: int) -> bool:
        return self.repo.delete(item_id)

# Simple dependency that you can wire into FastAPI with Depends(...)
def get_service() -> KeysService:
    # Swap this out for DI container / db session wired repository
    repo = KeysRepository()
    return KeysService(repo)
