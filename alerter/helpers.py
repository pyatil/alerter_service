import asyncio


def run(coro):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coro)
