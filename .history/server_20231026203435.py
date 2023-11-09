import asyncio

async def main():
    print('Sohum')

async def foo(text):
    print(text)
    await asyncio.sleep(1)

asyncio.run(foo('Sohum'))