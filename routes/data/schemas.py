from pydantic import BaseModel, Field
from typing import Optional, Literal
import datetime as dt

class AlertBase(BaseModel):
    contract: str = Field(..., description="Contract identifier, e.g., 'NQ1!'")
    trade_type: Literal['buy', 'sell', 'exit'] = Field(..., description="Type of trade")
    quantity: int = Field(..., gt=0, description="Quantity of the trade")
    price: float = Field(..., gt=0, description="Price at which the trade was executed")
    secret_key: Optional[str] = Field(None, description="Optional secret key for authentication")
    timestamp: Optional[dt.datetime] = Field(None, description="Timestamp of the alert")

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    contract: Optional[str] = Field(None, description="Contract identifier, e.g., 'NQ1!'")
    trade_type: Optional[Literal['buy', 'sell', 'exit']] = Field(None, description="Type of trade")
    quantity: Optional[int] = Field(None, gt=0, description="Quantity of the trade")
    price: Optional[float] = Field(None, gt=0, description="Price at which the trade was executed")
    secret_key: Optional[str] = Field(None, description="Optional secret key for authentication")
    timestamp: Optional[dt.datetime] = Field(None, description="Timestamp of the alert")

class AlertRead(AlertBase):
    id: str = Field(..., description="MongoDB document ID")

    class Config:
        from_attributes = True
