"""
FastAPI router providing data endpoints.

This module exposes a `data_router` (APIRouter) that other parts of the
application can include on the main FastAPI app. The file contains small,
well-documented route shells intended to be implemented further as needed.
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter, Body, Query
from pydantic import BaseModel

from models import FilterParams


data_router = APIRouter(prefix="/data", tags=["data"])


class PingResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str
    message: Optional[str] = None


class DataPayload(BaseModel):
    """Example request payload for data ingestion endpoints.

    Adjust fields to match the actual alert/data schema used by the project.
    """

    name: str
    timestamp: Optional[str] = None
    payload: Dict[str, Any] = {}


@data_router.get("/ping", response_model=PingResponse)
async def ping() -> PingResponse:
    """Health-check endpoint for the data router.

    Returns a simple JSON confirming the router is reachable. Useful for
    readiness/liveness checks and quick manual testing.
    """
    return PingResponse(status="ok", message="data router alive")


@data_router.post("/ingest", status_code=201)
async def ingest_data(item: DataPayload = Body(...)) -> Dict[str, Any]:
    """Ingest a single data item (placeholder).

    This is a minimal example endpoint that accepts a JSON payload. Replace
    the implementation with logic to validate, normalize, persist or forward
    the incoming alert/data to downstream processors.

    Returns a simple acknowledgement containing the provided name and
    a generated id (placeholder).
    """
    # TODO: persist/forward/process the payload
    ack = {"received": True, "name": item.name, "timestamp": item.timestamp}
    return ack


@data_router.get("/items", response_model=Dict[str, Any])
async def list_items(limit: int = Query(100, ge=1, le=1000), name: Optional[str] = None) -> Dict[str, Any]:
    """List recent data items (placeholder).

    Parameters
    - limit: maximum number of items to return
    - name: optional filter by `name` value
    """
    # TODO: query the data store and return results
    sample = {"count": 0, "items": [], "limit": limit, "filter_name": name}
    return sample


@data_router.post("/filters/normalize")
async def normalize_filters(params: FilterParams) -> dict:
    """Accept filter parameters and return the normalized kwargs usable by the
    internal filtering utilities.

    This endpoint demonstrates how FastAPI will parse and validate incoming
    JSON into the `FilterParams` Pydantic model, and how handlers can call
    `to_filter_kwargs` to obtain a dictionary suitable for passing to the
    `logic.alert_data.filters.filter_alert_data` function.
    """
    return params.to_filter_kwargs()
