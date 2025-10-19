from beanie import Document
from pydantic import Field, ConfigDict, AliasChoices
from typing import Literal, Optional, Dict
import datetime as dt
from pymongo import IndexModel
from core.constants import k

uniqueIndex = [
    (k.CONTRACT, 1),
    (k.TRADE_TYPE, 1),
    (k.QUANTITY, 1),
    (k.PRICE, 1),
    (k.TIMESTAMP, 1),
    (k.NAME.lower(), 1),
]

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
    name: Optional[str] = Field(
        default=None,
        description="Alert name",
        validation_alias=AliasChoices("name", "Name"),
    )

    # All alerts are compatible with Quantview Alerts
    userId: Optional[str] = Field(None, description="User identifier")
    strategy: Optional[int] = Field(0, description="Strategy identifier")
    spam_key: Optional[str] = Field(None, description="Spam key for filtering", alias="spam-key")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    class Settings:
        name = "alerts"  # Collection name in MongoDB
        indexes = [
            IndexModel(
                keys=uniqueIndex,
                unique=True,
            )
        ]
