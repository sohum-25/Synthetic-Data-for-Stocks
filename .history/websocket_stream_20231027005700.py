from fastapi import FastAPI
from fastapi_websocket import WebSocket
import random
import math
import time
import asyncio
import multiprocessing

app = FastAPI()

connected_clients = set()

# Data generation function
async def generate_tick_by_tick_data(symbol, S0, websocket: WebSocket):
    async def calculate_ltp():
        r = 0.05  # Interest rate
        sigma = 0.2  # Volatility
        T = 1.0  # Time

        z = random.gauss(0, 1)  # Random normal variable

        ltp = S0 * math.exp((r - 0.5 * sigma**2) * T + sigma * math.sqrt(T) * z)

        return round(ltp, 2)

    while websocket.client_state == WebSocket.client_connected:
        ticks_per_second = random.randint(1, 3)
        time_interval = 1 / ticks_per_second

        ltp = await calculate_ltp()

        tick_data = {
            "ltp": ltp,
            "symbol": symbol
        }

        await websocket.send_json(tick_data)
        await asyncio.sleep(time_interval)

# Create a list of configurations for 10 instances
configs = [
    {"symbol": "RELIANCE", "initial_price": 2500.00},
    # ... Add other symbols here ...
]

# Function to run the tick generator for each symbol
async def run_tick_generator(config, websocket: WebSocket):
    symbol = config["symbol"]
    initial_price = config["initial_price"]
    await generate_tick_by_tick_data(symbol, initial_price, websocket)

# WebSocket route for subscribing to tick data
@app.websocket_route("/subscribe/{symbol}")
async def subscribe(websocket: WebSocket, symbol: str):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        for config in configs:
            await run_tick_generator(config, websocket)
    except Exception:
        pass  # Handle exceptions if needed
    finally:
        connected_clients.remove(websocket)

# Start tick generators as separate processes
if __name__ == '__main__':
    processes = []

    for config in configs:
        process = multiprocessing.Process(target=run_tick_generator, args=(config,))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()
