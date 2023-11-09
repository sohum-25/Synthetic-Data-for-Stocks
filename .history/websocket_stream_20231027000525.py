from fastapi import FastAPI, WebSocket
import random
import math
import time
import asyncio

app = FastAPI()

connected_clients = set()

def generate_tick_by_tick_data(symbol, S0):
    while True:
        ticks_per_second = random.randint(1, 3)
        time_interval = 1 / ticks_per_second

        r = 0.05  # Interest rate
        sigma = 0.2  # Volatility
        T = 1.0  # Time

        z = random.gauss(0, 1)  # Random normal variable

        ltp = S0 * math.exp((r - 0.5 * sigma**2) * T + sigma * math.sqrt(T) * z)
        ltp = round(ltp, 2)

        tick_data = {
            "ltp": ltp,
            "symbol": symbol
        }

        for client in connected_clients:
            asyncio.create_task(client.send_json(tick_data))

        time.sleep(time_interval)

@app.websocket("/subscribe/{symbol}")
async def subscribe(websocket: WebSocket, symbol: str):
    await websocket.accept()
    connected_clients.add(websocket)

@app.websocket("/unsubscribe")
async def unsubscribe(websocket: WebSocket):
    connected_clients.discard(websocket)
    await websocket.close()

if __name__ == "__main__":
    import uvicorn

    # Create tick generators for each symbol
    for config in configs:
        symbol = config["symbol"]
        initial_price = config["initial_price"]
        ticker = generate_tick_by_tick_data(symbol, initial_price)
        asyncio.create_task(ticker)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
