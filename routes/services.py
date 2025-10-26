from pydantic import BaseModel, Field
from typing import Optional

from .data.schemas import AlertRead, AlertUpdate, AlertCreate
from .data.service import DataService, get_service as get_data_service

from .keys.service import KeysService, get_service as get_keys_service


class ServiceWorker(BaseModel):
    keys_service: KeysService = Field(get_keys_service(), description="Service for managing keys")
    data_service: DataService = Field(get_data_service(), description="Service for managing data")


    class Config:
        from_attributes = True  # pydantic v2 ORM mode

    async def create_alert(self, payload: AlertCreate, secret_key: str) -> AlertRead:

         # get name of strategy
        name = await self.keys_service.get_strategy_name_by_key(secret_key)

        # add secret key and name to payload
        payload.name = name
        payload.secret_key = secret_key
        return await self.data_service.create(payload)

