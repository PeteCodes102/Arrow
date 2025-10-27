from pydantic import BaseModel, Field
from typing import Optional

class KeysBase(BaseModel):
    secret_key: Optional[str] = None
    name: str
    description: Optional[str] = None

class KeysCreate(KeysBase):
    # Fields required only on create
    pass

class KeysUpdate(BaseModel):
    # All fields optional for partial update
    pass

class KeysRead(KeysBase):
    id: str = Field(..., description="Primary identifier")

    class Config:
        from_attributes = True  # pydantic v2 ORM mode
