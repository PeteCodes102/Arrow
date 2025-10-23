from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse

from .schemas import KeysCreate, KeysRead, KeysUpdate
from .service import KeysService, get_service

keys_router = APIRouter(prefix="/keys", tags=["keys"])

@keys_router.get("/{secret_key}", response_class=PlainTextResponse)
def get_strategy_name(secret_key: str, service: KeysService = Depends(get_service)):
    """
    Get strategy name by secret key.
    """
    return service.get_strategy_name(secret_key)

# @keys_router.get("/", response_model=List[KeysRead])
# def list_keys(service: KeysService = Depends(get_service)):
#     """
#     List keys items.
#     """
#     return service.list()
#
# @keys_router.get("/{item_id}", response_model=KeysRead)
# def get_keys(item_id: int, service: KeysService = Depends(get_service)):
#     """
#     Get a single keys item by ID.
#     """
#     item = service.get(item_id)
#     if item is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Keys not found")
#     return item
#
# @keys_router.post("/", response_model=KeysRead, status_code=status.HTTP_201_CREATED)
# def create_keys(payload: KeysCreate, service: KeysService = Depends(get_service)):
#     """
#     Create a new keys item.
#     """
#     return service.create(payload)
#
# @keys_router.put("/{item_id}", response_model=KeysRead)
# def update_keys(item_id: int, payload: KeysUpdate, service: KeysService = Depends(get_service)):
#     """
#     Update an existing keys item by ID.
#     """
#     updated = service.update(item_id, payload)
#     if updated is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Keys not found")
#     return updated
#
# @keys_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_keys(item_id: int, service: KeysService = Depends(get_service)):
#     """
#     Delete a keys item by ID.
#     """
#     deleted = service.delete(item_id)
#     if not deleted:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Keys not found")
#     return None
