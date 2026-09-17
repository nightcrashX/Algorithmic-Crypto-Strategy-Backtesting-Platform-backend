from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

# Query parameters pattern
@app.websocket("/indicator/ws/candles")
async def websocket_candles(
    websocket: WebSocket, 
    exchange: str, 
    symbol: str, 
    timeframe: str
):
    await websocket.accept()
    print(f"Client connected: {exchange} - {symbol} - {timeframe}")
    try:
        while True:
            # Your live data loop here
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        print("Client disconnected")