import asyncio
import random


async def f(n):
    tasks = (asyncio.ensure_future(get_content('a')), asyncio.ensure_future(get_content('b')), asyncio.ensure_future(get_content('c')),)  # 仕事の内容
    
    return n, await asyncio.gather(*tasks)


async def get_content(n):
    print("stat"+str(n))
    await asyncio.sleep(3)
    print(f'end{n}')
    return n


def main():
    loop = asyncio.get_event_loop()
    v = loop.run_until_complete(f(1))


if __name__ == "__main__":
    main()
