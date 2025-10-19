from typing import List, Optional

from core.constants import k
from core.logic import filtered_data_chart, db_data_to_df
from models.filters import FilterParams
from .schemas import AlertCreate, AlertRead, AlertUpdate, AlertQuery
from .repository import DataRepository
from .helpers import alert_processing_pipeline

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
        payload = await alert_processing_pipeline(payload)
        return await self.repo.create(payload)

    async def update(self, item_id: str, payload: AlertUpdate) -> Optional[AlertRead]:
        return await self.repo.update(item_id, payload)

    async def delete(self, item_id: str) -> bool:
        return await self.repo.delete(item_id)

    async def query(self, query: AlertQuery) -> List[AlertRead]:
        return await self.repo.query(query)

    async def generate_chart(self, filters: FilterParams):
        data = await self.repo.list()
        df = await db_data_to_df(data)
        chart_fig = await filtered_data_chart(df, "QGRID Elite - MNQ1! 1s Renko 2b ...", delta=5.0, flip=False, **filters.model_dump(exclude="name"))
        return chart_fig.to_dict()
    
    async def get_strategy_names(self) -> List[str]:
        data = await self.repo.list()
        df = await db_data_to_df(data)
        return df[k.NAME].dropna().unique().tolist()


# Dependency for FastAPI
async def get_service() -> DataService:
    repo = DataRepository()
    return DataService(repo)
