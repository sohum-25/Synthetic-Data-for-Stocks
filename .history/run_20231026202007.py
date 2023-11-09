import asyncio
import websockets

async def hello():
    uri="ws://localhost:3232"
    async with websockets.connect(uri) as websocket:
        name=input("Whats yo name nigga")

        await websocket.send(name)
        print(f'Client sent: {name}')

        greeting=await websocket.recv()
        print(f"Client received: {greeting}")


if __name__ =="__main__":
    asyncio.run(hello())