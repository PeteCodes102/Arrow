from pydantic import Field
from pydantic_settings import BaseSettings
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

    NAME: str = Field('Name', description='Alert name column')
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

    # .env file configuration
    MONGO_DB_CONNECTION_STRING: Optional[str] = Field(None, description='MongoDB connection string from environment')
    MONGO_DB_NAME: Optional[str] = Field(None, description='MongoDB database name from environment')
    MONGO_COLLECTION_NAME: Optional[str] = Field(None, description='MongoDB collection name')


    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()

BUY = settings.BUY
SELL = settings.SELL
EXIT = settings.EXIT

DATE_FORMAT = settings.DATE_FORMAT
TIME_FORMAT = settings.TIME_FORMAT
DATETIME_FORMAT = settings.DATETIME_FORMAT
NAME = settings.NAME
DESCRIPTION = settings.DESCRIPTION
TIME = settings.TIME
TIMESTAMP = settings.TIMESTAMP

PRICE = settings.PRICE
PROFIT = settings.PROFIT
rPROFIT = settings.rPROFIT
TRADE_TYPE = settings.TRADE_TYPE
QUANTITY = settings.QUANTITY
TradeType = settings.TradeType
SecretKey = settings.SecretKey
Timestamp = settings.Timestamp
AlgoDict = settings.AlgoDict