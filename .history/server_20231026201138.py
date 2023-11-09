import asyncio
import websockets

async def hello(websocket):
    name = await websocket.recv()
    print(f'Server recieved {name}')
    greeting=f'Hello{name}'

    await websocket.send(greeting)
    print(f'Server Sent:{greeting}')


async def main():
    async with websockets.serve(hello,"localhost",8765):
        await asyncio.Future()


if __name__=="  main  ":
    asyncio.run(main())
    