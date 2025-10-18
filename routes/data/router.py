from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from models.filters import FilterParams
from .schemas import AlertCreate, AlertRead, AlertUpdate, AlertQuery, ChartData
from .service import DataService, get_service

data_router = APIRouter(prefix="/data", tags=["data"])

@data_router.get("/", response_model=List[AlertRead])
async def list_data(service: DataService = Depends(get_service)):
    """
    List data items.
    """
    return await service.list()

@data_router.get("/{item_id}", response_model=AlertRead)
async def get_data(item_id: str, service: DataService = Depends(get_service)):
    """
    Get a single data item by ID.
    """
    item = await service.get(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return item

@data_router.get("/strategy-names/all", response_model=List[str])
async def get_strategy_names(service: DataService = Depends(get_service)):
    """
    Get unique strategy names from data items.
    """
    return await service.get_strategy_names()

@data_router.post("/", response_model=AlertRead, status_code=status.HTTP_201_CREATED)
async def create_data(payload: AlertCreate, service: DataService = Depends(get_service)):
    """
    Create a new data item.
    """
    return await service.create(payload)

@data_router.put("/{item_id}", response_model=AlertRead)
async def update_data(item_id: str, payload: AlertUpdate, service: DataService = Depends(get_service)):
    """
    Update an existing data item by ID.
    """
    updated = await service.update(item_id, payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return updated

@data_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(item_id: str, service: DataService = Depends(get_service)):
    """
    Delete a data item by ID.
    """
    deleted = await service.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return None

@data_router.post("/chart/filters", response_model=ChartData)
async def get_chart_data(filters: FilterParams, service: DataService = Depends(get_service)):
    """
    Get data formatted for charting.
    """
    chart_json = await service.generate_chart(filters)
    return {"chart_json": chart_json}
