import asyncio

async def main():
    print('Sohum')
    await foo('ktwe')
    print('Finished')
async def foo(text):
    print(text)
    await asyncio.sleep(10)

asyncio.run(main())