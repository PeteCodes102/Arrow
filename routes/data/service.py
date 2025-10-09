from typing import List, Optional
from .schemas import AlertCreate, AlertRead, AlertUpdate
from .repository import DataRepository

class DataService:
    """
    Business logic layer for data, using async Beanie repository.
    """
    def __init__(self, repo: DataRepository):
        self.repo = repo

    async def list(self) -> List[AlertRead]:
        return await self.repo.list()

    async def get(self, item_id: str) -> Optional[AlertRead]:
        return await self.repo.get(item_id)

    async def create(self, payload: AlertCreate) -> AlertRead:
        return await self.repo.create(payload)

    async def update(self, item_id: str, payload: AlertUpdate) -> Optional[AlertRead]:
        return await self.repo.update(item_id, payload)

    async def delete(self, item_id: str) -> bool:
        return await self.repo.delete(item_id)

# Dependency for FastAPI
async def get_service() -> DataService:
    repo = DataRepository()
    return DataService(repo)
