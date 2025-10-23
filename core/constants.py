from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Optional, Dict, Type, ClassVar
import datetime as dt


class Settings(BaseSettings):
    """
    Project-wide configuration and constants. Use as a singleton via Settings().
    Supports environment variable overrides for deployment flexibility.
    """
    BUY: str = Field('buy', description='Buy signal token')
    SELL: str = Field('sell', description='Sell signal token')
    EXIT: str = Field('exit', description='Exit signal token')

    DATE_FORMAT: str = Field('%Y-%m-%d', description='Date format string')
    TIME_FORMAT: str = Field('%H:%M:%S', description='Time format string')
    DATETIME_FORMAT: str = Field('%Y-%m-%d %H:%M:%S', description='Datetime format string')

    TICKER: str = Field('Ticker', description='Ticker column')
    CONTRACT: str = Field('contract', description='Contract column')
    NAME: str = Field('Name', description='Alert name column', alias="name")
    DESCRIPTION: str = Field('Description', description='Alert description column')
    TIME: str = Field('Time', description='Alert time column')
    TIMESTAMP: str = Field('timestamp', description='Timestamp column')
    PRICE: str = Field('price', description='Price column')
    PROFIT: str = Field('profit', description='Profit column')
    rPROFIT: str = Field('rProfit', description='Running profit column')
    TRADE_TYPE: str = Field('trade_type', description='Trade type column')
    QUANTITY: str = Field('quantity', description='Quantity column')

    # Types

    TradeType: ClassVar = Literal['buy', 'sell', 'exit']
    SecretKey: ClassVar = Optional[str]
    Timestamp: ClassVar = Optional[dt.datetime]
    AlgoDict: ClassVar = Dict[str, dt.datetime | str | float | int | TradeType]
    SecretKeyIndex: ClassVar = Dict[str, str]

    # .env file configuration
    MONGO_DB_CONNECTION_STRING: Optional[str] = Field(None, description='MongoDB connection string from environment')
    MONGO_DB_NAME: Optional[str] = Field('alertDb', description='MongoDB database name from environment')
    MONGO_COLLECTION_NAME: Optional[str] = Field(None, description='MongoDB collection name')

    model_config = SettingsConfigDict(
        env_file='../.env',
        env_file_encoding='utf-8',
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra='allow'
    )


k = Settings()

BUY = k.BUY
SELL = k.SELL
EXIT = k.EXIT

DATE_FORMAT = k.DATE_FORMAT
TIME_FORMAT = k.TIME_FORMAT
DATETIME_FORMAT = k.DATETIME_FORMAT
NAME = k.NAME
DESCRIPTION = k.DESCRIPTION
TIME = k.TIME
TIMESTAMP = k.TIMESTAMP

PRICE = k.PRICE
PROFIT = k.PROFIT
rPROFIT = k.rPROFIT
TRADE_TYPE = k.TRADE_TYPE
QUANTITY = k.QUANTITY
TradeType = k.TradeType
SecretKey = k.SecretKey
Timestamp = k.Timestamp
AlgoDict = k.AlgoDict
SecretKeyIndex = k.SecretKeyIndex