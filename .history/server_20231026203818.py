import asyncio

async def main():
    print('Sohum')
    task = asyncio.create_task(foo('Muley'))
    await task
    print('Finished')
async def foo(text):
    print(text)
    await asyncio.sleep(1)

asyncio.run(main())