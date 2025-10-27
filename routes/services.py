from pydantic import BaseModel, Field, ConfigDict
from typing import Union, List
from fastapi import HTTPException, status

from .data.schemas import AlertRead, AlertCreate
from .data.service import DataService, get_service as get_data_service
from .keys.helpers import generate_secret_key
from .keys.schemas import KeysCreate, KeysRead
from .keys.service import KeysService, get_service as get_keys_service


class ServiceWorker(BaseModel):
    """
    Orchestration layer that coordinates multiple services for complex operations.
    This keeps individual services decoupled while allowing cross-service workflows.
    """
    keys_service: KeysService = Field(..., description="Service for managing keys")
    data_service: DataService = Field(..., description="Service for managing data")

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    async def create_alert(self, payload: AlertCreate, secret_key: str) -> AlertRead:
        """
        Create an alert with automatic strategy name lookup via secret key.

        Args:
            payload: The alert creation data
            secret_key: The secret key to identify the strategy

        Returns:
            The created alert

        Raises:
            HTTPException: If the secret key is invalid
        """
        # Get name of strategy
        name = await self.keys_service.get_name_by_key(secret_key)

        if not name:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid secret key provided."
            )

        # Add secret key and name to payload
        payload.name = name
        payload.secret_key = secret_key
        return await self.data_service.create(payload)

    async def bind_key_to_name(self, name: str) -> Union[KeysRead, dict]:
        """
        Bind a new secret key to a strategy name.

        Args:
            name: The strategy name to bind

        Returns:
            The created key or a message if the name is already bound
        """
        # Check if name already has a key
        existing_keys = await self.keys_service.repo.search_by_name(name)
        if existing_keys:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Strategy name '{name}' is already bound to a secret key."
            )

        # Generate new secret key
        secret_key = generate_secret_key()
        payload = KeysCreate(
            secret_key=secret_key,
            name=name,
            description="Auto-generated key"
        )
        return await self.keys_service.create(payload)

    async def get_strategy_names(self) -> List[str]:
        """Get all unique strategy names from alerts."""
        return await self.data_service.get_strategy_names()


async def get_service_worker() -> ServiceWorker:
    """Dependency injection for ServiceWorker."""
    return ServiceWorker(
        keys_service=await get_keys_service(),
        data_service=await get_data_service()
    )


