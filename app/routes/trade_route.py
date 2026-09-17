# trade_route.py

from fastapi import APIRouter, HTTPException , Query

from app.services.trade_service import trading
from app.schemas.trade_schema import Trade
from app.services.trade_service import get_or_create_demo_account
from app.services.trade_service import update_balance
from app.services.trade_service import get_trade_history

trade_router = APIRouter(
    prefix="/trade",
    tags=["Demo Trading"]
)


@trade_router.post("/trade")
async def create_trade(body: Trade):

    try:
        result = trading(body)

        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@trade_router.get("/account")
async def get_demo_account():
    account = get_or_create_demo_account()
    return {
        "balance": account["balance"],
        "positions": account.get("positions", {}),
    }

@trade_router.get("/account/updatebalance")
async def get_demo_account(balance):  
    return update_balance(balance=balance)

@trade_router.get("/history")
async def trade_history(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    from_date: str | None = None,
    to_date: str | None = None,
):
    return get_trade_history(
        page=page,
        limit=limit,
        from_date=from_date,
        to_date=to_date,
    )