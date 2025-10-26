from typing import List, Optional
from .schemas import KeysCreate, KeysRead, KeysUpdate
from .repository import KeysRepository
from .helpers import generate_secret_key

class KeysService:
    """
    Business logic layer for keys.
    """
    def __init__(self, repo: KeysRepository):
        self.repo = repo

    async def list(self) -> List[KeysRead]:
        return self.repo.list()

    async def get(self, item_id: int) -> Optional[KeysRead]:
        return self.repo.get(item_id)

    async def create(self, payload: KeysCreate) -> KeysRead:
        return self.repo.create(payload)

    async def update(self, item_id: int, payload: KeysUpdate) -> Optional[KeysRead]:
        return self.repo.update(item_id, payload)

    async def delete(self, item_id: int) -> bool:
        return self.repo.delete(item_id)

    async def get_name_by_key(self, secret_key: str) -> Optional[str]:
        # Optimized: query the repository for the item with the matching secret_key
        secret_key_index = await self.repo.search(first=True, secret_key=secret_key)
        if secret_key_index:
            return secret_key_index.name
        return None

# Simple dependency that you can wire into FastAPI with Depends(...)
def get_service() -> KeysService:
    # Swap this out for DI container / db session wired repository
    repo = KeysRepository()
    return KeysService(repo)
