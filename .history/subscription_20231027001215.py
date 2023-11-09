import asyncio
import websockets

async def subscribe_to_tick_data(symbol):
    async with websockets.connect(f"ws://your_server_address/subscribe/{symbol}") as websocket:
        while True:
            tick_data = await websocket.recv()
            print(f"Received Tick Data for {symbol}: {tick_data}")

if __name__ == "__main__":
    symbol_to_subscribe = "RELIANCE"  # Replace with the symbol you want to subscribe to
    asyncio.get_event_loop().run_until_complete(subscribe_to_tick_data(symbol_to_subscribe))
