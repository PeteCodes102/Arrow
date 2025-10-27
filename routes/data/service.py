import json
from typing import List, Optional
import logging

from fastapi import HTTPException
from starlette import status

from core.constants import k
from core.logic import filtered_data_chart, db_data_to_df
from models.filters import FilterParams
from models.secret_key import SecretKeyIndex
from .schemas import AlertCreate, AlertRead, AlertUpdate, AlertQuery
from .repository import DataRepository
from .helpers import alert_processing_pipeline

logger = logging.getLogger(__name__)


class DataService:
    """
    Business logic layer for trading alerts using async Beanie repository.

    This service handles alert operations including CRUD, querying, and chart generation.
    """
    def __init__(self, repo: DataRepository):
        self.repo = repo

    async def list(self, limit: Optional[int] = None) -> List[AlertRead]:
        """
        List all alerts with optional limit.

        Args:
            limit: Maximum number of alerts to return

        Returns:
            List of alerts
        """
        return await self.repo.list(limit=limit)

    async def get(self, item_id: str) -> Optional[AlertRead]:
        """Get a single alert by ID."""
        return await self.repo.get(item_id)

    async def create(self, payload: AlertCreate) -> AlertRead:
        """
        Create a new alert with processing pipeline.

        Args:
            payload: Alert creation data

        Returns:
            The created alert
        """
        try:
            payload = await alert_processing_pipeline(payload)
            return await self.repo.create(payload)
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create alert: {str(e)}"
            )

    async def create_with_secret_key(self, secret_key: str, payload: AlertCreate) -> AlertRead:
        """
        Create an alert with secret key authentication.

        This method looks up the strategy name associated with the secret key
        and automatically populates the alert with this information.

        Args:
            secret_key: The secret key for authentication
            payload: Alert creation data

        Returns:
            The created alert

        Raises:
            HTTPException: If the secret key is invalid
        """
        # Look up the strategy name from the secret key
        key_doc = await SecretKeyIndex.find_one(SecretKeyIndex.secret_key == secret_key)

        if not key_doc:
            logger.warning(f"Invalid secret key attempted: {secret_key[:10]}...")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid secret key provided"
            )

        # Populate the alert with strategy information
        payload.name = key_doc.name
        payload.secret_key = secret_key

        logger.info(f"Creating alert for strategy: {key_doc.name}")
        return await self.create(payload)

    async def update(self, item_id: str, payload: AlertUpdate) -> Optional[AlertRead]:
        """Update an existing alert."""
        return await self.repo.update(item_id, payload)

    async def delete(self, item_id: str) -> bool:
        """Delete an alert by ID."""
        return await self.repo.delete(item_id)

    async def query(self, query: AlertQuery) -> List[AlertRead]:
        """Query alerts with filters."""
        return await self.repo.query(query)

    async def generate_chart(self, filters: FilterParams):
        """
        Generate chart data for filtered alerts.

        Args:
            filters: Filter parameters for the chart

        Returns:
            Plotly chart JSON data
        """
        try:
            data = await self.repo.list()
            df = await db_data_to_df(data)
            chart_fig = await filtered_data_chart(
                df,
                delta=5.0,
                flip=False,
                **filters.model_dump()
            )

            # Convert to JSON and ensure proper structure
            import plotly.io as pio
            chart_dict = pio.to_json(chart_fig, pretty=False)
            chart_json = json.loads(chart_dict)

            if 'data' not in chart_json:
                chart_json['data'] = []

            return chart_json
        except Exception as e:
            logger.error(f"Error generating chart: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate chart: {str(e)}"
            )

    async def get_strategy_names(self) -> List[str]:
        """
        Get all unique strategy names from alerts.

        Returns:
            List of unique strategy names
        """
        try:
            data = await self.repo.list()
            if not data:
                return []

            df = await db_data_to_df(data)
            return df[k.NAME].dropna().unique().tolist()
        except Exception as e:
            logger.error(f"Error getting strategy names: {e}")
            return []


async def get_service() -> DataService:
    """Dependency injection for DataService."""
    repo = DataRepository()
    return DataService(repo)
