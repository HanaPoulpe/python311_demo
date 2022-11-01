import asyncio


async def coro(m):
    return m


async def main():
    async with asyncio.TaskGroup() as g:
        r1 = g.create_task(coro("r1"))
        r2 = g.create_task(coro("r2"))

    print(r1.result())
    print(await r2)


if __name__ == '__main__':
    asyncio.run(main())
