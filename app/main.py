#main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth_route import user_routes
from app.routes.exchange_route import exchange_router
from app.middleware.auth_middleware import AuthMiddleware
from app.routes.indicator_route import indicator_router
from app.routes.wb_routes import ws_router

from app.routes.trade_route import trade_router
from app.routes.test_wb import live_candle_route

app = FastAPI()

origins = [
    "http://localhost:5173",  # Default Vite port
    "http://localhost:8000",  # Default Create React App port
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
    "ws://127.0.0.1:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hybridaction/zybTrackerStatisticsAction")
def tracker_statistics(data: str = None, __callback__: str = None):
    return {"status": "success", "message": "Tracker data received"}


@app.get('/')
def home():
    return {"message":"running"}

app.include_router(live_candle_route)

app.add_middleware(AuthMiddleware)

app.include_router(user_routes)

app.include_router(exchange_router)

app.include_router(indicator_router)

app.include_router(ws_router)

app.include_router(trade_router)



