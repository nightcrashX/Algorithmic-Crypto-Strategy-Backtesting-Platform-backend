# indicator_schema.py
from typing import Any
from pydantic import BaseModel, Field

class IndicatorItem(BaseModel):
    id: str
    type: str
    settings: dict[str, Any] = Field(default_factory=dict)

class IndicatorRequest(BaseModel):
    exchange: str
    symbol: str
    timeframe: str
    indicators: list[IndicatorItem]