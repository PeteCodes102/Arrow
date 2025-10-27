from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from .data.schemas import AlertRead, AlertUpdate, AlertCreate
from .data.service import DataService, get_service as get_data_service
from .keys.helpers import generate_secret_key
from .keys.schemas import KeysCreate, KeysRead

from .keys.service import KeysService, get_service as get_keys_service


class ServiceWorker(BaseModel):
    keys_service: KeysService = Field(..., description="Service for managing keys")
    data_service: DataService = Field(..., description="Service for managing data")

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )


    async def create_alert(self, payload: AlertCreate, secret_key: str) -> AlertRead:

         # get name of strategy
        name = await self.keys_service.get_name_by_key(secret_key)

        if not name:
            raise ValueError("Invalid secret key provided.")
        # add secret key and name to payload
        payload.name = name
        payload.secret_key = secret_key
        return await self.data_service.create(payload)

    async def bind_key_to_name(self, name: str) -> KeysRead | dict:
        # check if name already has a key
        existing_keys = await self.keys_service.repo.search(name=name)
        if existing_keys:
            return {"message": f"Name '{name}' is already bound to a secret key."}
        secret_key = generate_secret_key()
        payload = KeysCreate(secret_key=secret_key, name=name, description="auto-generated key")
        return await self.keys_service.create(payload)

    async def get_strategy_names(self):
        return await self.data_service.get_strategy_names()


async def get_service_worker() -> ServiceWorker:
    return ServiceWorker(
        keys_service= await get_keys_service(),
        data_service=await get_data_service()
    )


