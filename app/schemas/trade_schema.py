# trade_schema.py

from pydantic import BaseModel, Field
from typing import Literal


class Trade(BaseModel):
    trade_type: Literal["BUY", "SELL"]
    exchange: str
    symbol: str

    price: float = Field(gt=0)
    quantity: float = Field(gt=0)