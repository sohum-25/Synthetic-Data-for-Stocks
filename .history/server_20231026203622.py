import asyncio

async def main():
    print('Sohum')
    await foo('Muley')
    print('Finished')
async def foo(text):
    print(text)
    await asyncio.sleep(1)

asyncio.run(main())