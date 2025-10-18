# init a database using motor
from motor.motor_asyncio import AsyncIOMotorClient

from pydantic import BaseModel, Field, ConfigDict, ValidationError
from typing import Literal, Optional
import datetime as dt

import asyncio
from core.logic import load_data_from_csv_util

class BaseAlert(BaseModel):
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
    Name: Optional[str] = Field(..., description="Alert name", alias="name")

    # All alerts are compatible with Quantview Alerts
    userId: Optional[str] = Field(None, description="User identifier")
    strategy: Optional[int] = Field(0, description="Strategy identifier")
    spam_key: Optional[str] = Field(None, description="Spam key for filtering", alias="spam-key")

    model_config = ConfigDict(arbitrary_types_allowed=True)


# load df from a csv file

# def document

async def init_db():
    client = AsyncIOMotorClient("mongodb+srv://pmailcodetest:J0PvfyHSnlm3xXr7@cluster0.ss2odgw.mongodb.net/")
    db = client['alertDb']
    collection = db['alerts']
    return collection

async def create_item(collection, item: BaseAlert) -> dict:
    """
    Insert a new document into the collection.
    """
    item_dict = item.model_dump()
    result = await collection.insert_one(item_dict)
    item_dict['_id'] = str(result.inserted_id)
    return item_dict

async def main():
    collection = await init_db()
    df = load_data_from_csv_util('tv_alerts.csv')
    count = 0

    for index, row in df.iterrows():
        row_dict = row.to_dict()
        try:
            alert = BaseAlert(**row_dict)
            created_item = await create_item(collection, alert)
            print(f"Created Item: {count + 1}; Name: {created_item['name']}")
            count += 1
        except ValidationError or Exception as e:
            print(f"Validation error at row {index}: {e}")
            print(f"Row data: {row_dict}")
            continue




if __name__ == "__main__":
    asyncio.run(main())