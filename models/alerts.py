from beanie import Document
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional, Dict
import datetime as dt

class BaseAlert(Document):
    """
    MongoDB document model for a trading alert.

    Fields:
        contract (str): Contract identifier, e.g., 'NQ1!'.
        trade_type (Literal['buy', 'sell', 'exit']): Type of trade.
        quantity (int): Quantity of the trade (must be > 0).
        price (float): Price at which the trade was executed (must be > 0).
        secret_key (Optional[str]): Optional secret key for authentication.
        timestamp (Optional[datetime]): Timestamp of the alert.
    """
    contract: str = Field(..., description="Contract identifier, e.g., 'NQ1!'")
    trade_type: Literal['buy', 'sell', 'exit'] = Field(..., description="Type of trade")
    quantity: int = Field(..., gt=0, description="Quantity of the trade")
    price: float = Field(..., gt=0, description="Price at which the trade was executed")
    secret_key: Optional[str] = Field(None, description="Optional secret key for authentication")
    timestamp: Optional[dt.datetime] = Field(None, description="Timestamp of the alert")

    model_config = ConfigDict(arbitrary_types_allowed=True)

class QVStyleAlert(BaseAlert):
    """
    MongoDB document model for a QV-style trading alert, extending BaseAlert.

    Fields:
        userId (Optional[str]): User identifier.
        strategy (Optional[int]): Strategy identifier (default 0).
        spam_key (Optional[str]): Spam key for filtering (aliased as 'spam-key').
    """
    userId: Optional[str] = Field(..., description="User identifier")
    strategy: Optional[int] = Field(0, description="Strategy identifier")
    spam_key: Optional[str] = Field(..., description="Spam key for filtering", alias="spam-key")

    def __init__(self, **data):
        if 'trade_type' in data:
            data['trade_type'] = data['trade_type'].lower()
        super().__init__(**data)
