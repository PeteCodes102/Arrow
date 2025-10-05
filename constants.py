from typing import Literal, Optional
import datetime as dt

BUY = 'buy'
SELL = 'sell'
EXIT = 'exit'

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATETIME_FORMAT = f'{DATE_FORMAT} {TIME_FORMAT}'

NAME = 'Name'
DESCRIPTION = 'Description'
TIME = 'Time'
TIMESTAMP = 'timestamp'
PRICE = 'price'
PROFIT = 'profit'
rPROFIT = 'rProfit'
TRADE_TYPE = 'trade_type'
QUANTITY = 'quantity'


# Types
TradeType = Literal['buy', 'sell', 'exit']
SecretKey = Optional[str]
Timestamp = Optional[dt.datetime]
AlgoDict = dict[str, dt.datetime | str | float | int | TradeType]