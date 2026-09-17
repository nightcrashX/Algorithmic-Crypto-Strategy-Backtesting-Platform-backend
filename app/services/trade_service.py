# trade_service.py

from datetime import datetime,time, timezone
from zoneinfo import ZoneInfo

from fastapi import HTTPException

from app.config.database import (
    get_trade_collection,
    get_demo_account_collection
)

from app.schemas.trade_schema import Trade
from app.config.settings import INITIAL_CAPITAL


trade_collection = get_trade_collection()
demo_account_collection = get_demo_account_collection()

def get_or_create_demo_account():

    account = demo_account_collection.find_one({
        "account_type": "demo"
    })

    if account:
        return account

    account = {
        "account_type": "demo",
        "balance": INITIAL_CAPITAL,
        "positions": {},
        # "created_at": datetime.now(timezone.utc)
        "created_at": datetime.now(
            ZoneInfo("Asia/Kolkata")
        )
    }

    result = demo_account_collection.insert_one(account)

    account["_id"] = result.inserted_id

    # print("account " , account)
    return account


def update_balance(balance):

    result = demo_account_collection.update_one(
        {
            "account_type": "demo"
        },
        {
            "$set": {
                "balance": float(balance)
            }
        }
    )

    if result.matched_count == 0:
        return {
            "success": False,
            "message": "Demo account not found"
        }

    account = demo_account_collection.find_one(
        {
            "account_type": "demo"
        },
        {
            "_id": 0
        }
    )

    return {
        "success": True,
        "message": "Balance updated successfully",
        "account": account
    }    
    
    


def trading(body: Trade):

    try:

        # --------------------------------------------------
        # 1. Get demo account
        # --------------------------------------------------

        account = get_or_create_demo_account()

        # print(account)
        balance = float(account["balance"])

        positions = account.get("positions", {})

        symbol = body.symbol.upper()
        trade_type = body.trade_type.upper()

        price = float(body.price)
        quantity = float(body.quantity)

        total = price * quantity

        # --------------------------------------------------
        # 2. BUY
        # --------------------------------------------------

        if trade_type == "BUY":

            if total > balance:

                raise HTTPException(
                    status_code=400,
                    detail={
                        "message": "Insufficient demo balance",
                        "available_balance": balance,
                        "required_amount": total
                    }
                )

            # Deduct money
            new_balance = balance - total

            # Existing position
            old_position = positions.get(
                symbol,
                {
                    "quantity": 0.0,
                    "average_price": 0.0
                }
            )

            old_quantity = float(
                old_position.get("quantity", 0)
            )

            old_average_price = float(
                old_position.get("average_price", 0)
            )

            new_quantity = old_quantity + quantity

            # Calculate new average price
            if new_quantity > 0:

                new_average_price = (
                    (
                        old_quantity * old_average_price
                    )
                    +
                    (
                        quantity * price
                    )
                ) / new_quantity

            else:

                new_average_price = price

            positions[symbol] = {
                "quantity": new_quantity,
                "average_price": new_average_price
            }

        # --------------------------------------------------
        # 3. SELL
        # --------------------------------------------------

        elif trade_type == "SELL":

            old_position = positions.get(symbol)

            if not old_position:

                raise HTTPException(
                    status_code=400,
                    detail=f"No position available for {symbol}"
                )

            old_quantity = float(
                old_position.get("quantity", 0)
            )

            if quantity > old_quantity:

                raise HTTPException(
                    status_code=400,
                    detail={
                        "message": "Insufficient asset quantity",
                        "symbol": symbol,
                        "available_quantity": old_quantity,
                        "requested_quantity": quantity
                    }
                )

            # Add money from selling
            new_balance = balance + total

            remaining_quantity = (
                old_quantity - quantity
            )

            if remaining_quantity <= 0:

                positions.pop(symbol, None)

            else:

                positions[symbol] = {
                    "quantity": remaining_quantity,
                    "average_price": old_position[
                        "average_price"
                    ]
                }

        else:

            raise HTTPException(
                status_code=400,
                detail="trade_type must be BUY or SELL"
            )

        # --------------------------------------------------
        # 4. Generate server timestamp
        # --------------------------------------------------

        trade_time = datetime.now(
            ZoneInfo("Asia/Kolkata")
        )

        # --------------------------------------------------
        # 5. Save trade
        # --------------------------------------------------

        trade_document = {
            "trade_type": trade_type,
            "exchange": body.exchange,
            "symbol": symbol,
            "price": price,
            "quantity": quantity,
            "total": total,
            "trade_time": trade_time,
            "account_type": "demo"
        }

        result = trade_collection.insert_one(
            trade_document
        )

        # --------------------------------------------------
        # 6. Update account
        # --------------------------------------------------
 
        demo_account_collection.update_one(
            {
                "_id": account["_id"]
            },
            {
                "$set": {
                    "balance": new_balance,
                    "positions": positions,
                    "updated_at": trade_time
                }
            }
        )

        # --------------------------------------------------
        # 7. Return result
        # --------------------------------------------------

        return {
            "success": True,
            "message": f"{trade_type} trade executed successfully",

            "trade": {
                "trade_id": str(result.inserted_id),
                "trade_type": trade_type,
                "exchange": body.exchange,
                "symbol": symbol,
                "price": price,
                "quantity": quantity,
                "total": total,
                "trade_time": trade_time.isoformat()
            },

            "account": {
                "balance": new_balance,
                "positions": positions
            }
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

from datetime import datetime, time
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")


def get_trade_history(
    page=1,
    limit=10,
    from_date=None,
    to_date=None,
):
    try:

        query = {
            "account_type": "demo"
        }

        # --------------------------------------------------
        # Date filter - Asia/Kolkata
        # --------------------------------------------------

        if from_date or to_date:

            trade_time_filter = {}

            if from_date:
                start_date = datetime.combine(
                    datetime.strptime(
                        from_date,
                        "%Y-%m-%d"
                    ).date(),
                    time.min,
                    tzinfo=IST
                )

                trade_time_filter["$gte"] = start_date

            if to_date:
                end_date = datetime.combine(
                    datetime.strptime(
                        to_date,
                        "%Y-%m-%d"
                    ).date(),
                    time.max,
                    tzinfo=IST
                )

                trade_time_filter["$lte"] = end_date

            query["trade_time"] = trade_time_filter

        # --------------------------------------------------
        # Pagination
        # --------------------------------------------------

        skip = (page - 1) * limit

        total_trades = trade_collection.count_documents(
            query
        )

        trades = list(
            trade_collection
            .find(query, {"_id": 0})
            .sort("trade_time", -1)
            .skip(skip)
            .limit(limit)
        )

        # --------------------------------------------------
        # Convert MongoDB UTC → Asia/Kolkata
        # --------------------------------------------------

        for trade in trades:

            trade_time = trade.get("trade_time")

            if trade_time:

                # MongoDB normally returns UTC datetime
                trade_time = trade_time.replace(
                    tzinfo=ZoneInfo("UTC")
                )

                trade["trade_time"] = (
                    trade_time
                    .astimezone(IST)
                    .isoformat()
                )

        # --------------------------------------------------
        # Pagination information
        # --------------------------------------------------

        total_pages = (
            (total_trades + limit - 1) // limit
            if total_trades
            else 0
        )

        return {
            "success": True,

            "data": trades,

            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_trades,
                "total_pages": total_pages,
            }
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }