from typing import List
from fastapi import APIRouter, status, Depends
from pydantic import BaseModel, Field

from .data.schemas import AlertRead, AlertCreate
from .keys.schemas import KeysRead
from .services import get_service_worker, ServiceWorker


alert_router = APIRouter(prefix="/alerts", tags=["alerts"])


class BindKeyRequest(BaseModel):
    """Request model for binding a key to a strategy name."""
    name: str = Field(..., description="Strategy name to bind to a new secret key")


@alert_router.get(
    "/strategy_names",
    response_model=List[str],
    summary="Get all strategy names",
    description="Retrieve a list of all unique strategy names from alerts."
)
async def get_strategy_names(
    services: ServiceWorker = Depends(get_service_worker)
) -> List[str]:
    """Get unique strategy names from alerts."""
    return await services.get_strategy_names()


@alert_router.post(
    "/create/{secret_key}",
    response_model=AlertRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create alert with secret key",
    description="Create a new alert associated with a strategy using the secret key for authentication."
)
async def create_alert(
    secret_key: str,
    payload: AlertCreate,
    services: ServiceWorker = Depends(get_service_worker)
) -> AlertRead:
    """
    Create a new alert associated with a strategy using the secret key.

    The secret key is used to:
    - Authenticate the request
    - Automatically associate the alert with the correct strategy name
    """
    return await services.create_alert(payload, secret_key)


@alert_router.post(
    "/bind_key",
    response_model=KeysRead,
    status_code=status.HTTP_201_CREATED,
    summary="Bind secret key to strategy",
    description="Generate and bind a new secret key to a strategy name."
)
async def bind_key_to_name(
    payload: BindKeyRequest,
    services: ServiceWorker = Depends(get_service_worker)
) -> KeysRead:
    """
    Bind a new secret key to a strategy name.

    This generates a cryptographically secure secret key and associates it
    with the provided strategy name. The key can then be used to create
    alerts for this strategy.
    """
    return await services.bind_key_to_name(payload.name)
