from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from .data.schemas import AlertRead, AlertCreate
from .keys.schemas import KeysCreate, KeysRead
from .services import get_service_worker


alert_router = APIRouter(prefix="/alerts", tags=["alerts"])

@alert_router.get("/strategy_names")
async def get_strategy_names(
    services=Depends(get_service_worker)
) -> List[str]:
    """
    Get unique strategy names from alerts.
    """
    return await services.get_strategy_names()

@alert_router.post("/create/{secret_key}", response_model=AlertRead, status_code=status.HTTP_201_CREATED)
async def create_alert(
    secret_key: str,
    payload: AlertCreate,
    services=Depends(get_service_worker)
):
    """
    Create a new alert associated with a strategy using the secret key.
    """
    return await services.create_alert(payload, secret_key)

@alert_router.post("/bind_key", response_model=KeysRead | dict, status_code=status.HTTP_201_CREATED)
async def bind_key_to_name(
    payload: KeysCreate,
    services=Depends(get_service_worker)
) -> KeysRead:
    """
    Bind a new secret key to a strategy name.
    """
    name = payload.name
    keys_read = await services.bind_key_to_name(name)
    return keys_read
