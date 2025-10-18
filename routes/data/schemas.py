from pydantic import BaseModel, Field
from typing import Optional, Literal, Any, Dict
import datetime as dt

class AlertBase(BaseModel):
    contract: str = Field(..., description="Contract identifier, e.g., 'NQ1!'")
    trade_type: Literal['buy', 'sell', 'exit'] = Field(..., description="Type of trade")
    quantity: int = Field(..., gt=0, description="Quantity of the trade")
    price: float = Field(..., gt=0, description="Price at which the trade was executed")
    secret_key: Optional[str] = Field(None, description="Optional secret key for authentication")
    timestamp: Optional[dt.datetime] = Field(None, description="Timestamp of the alert")
    Name: Optional[str] = Field(None, description="Alert name", alias="name")

class AlertCreate(AlertBase):
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    spam_key: Optional[str] = Field(None, description="Optional spam key for rate limiting", alias="spam-key")
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

class AlertQuery(BaseModel):
    user_id: Optional[str] = None
    strategy_name: Optional[str] = None
    options: Optional[dict] = None  # For easy customization of future query fields

class ChartData(BaseModel):
    # You can customize this schema to match your chart data structure
    chart_json: Dict[str, Any]
