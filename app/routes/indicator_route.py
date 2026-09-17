# indicator_route.py
from fastapi import APIRouter

from app.schemas.indicator_schema import IndicatorRequest
from app.services.indicator_service import get_indicators

from app.indicator_registry.indicator_registry import get_registry_metadata


indicator_router = APIRouter(
    prefix="/indicator",
    tags=["INDICATORs"]
)


@indicator_router.post("/")
def indicator(req: IndicatorRequest):
    return get_indicators(req)


@indicator_router.get("/registry")
def indicator_registry():
    return get_registry_metadata()