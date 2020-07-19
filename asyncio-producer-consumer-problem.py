import asyncio
import random
import time
import os
import itertools as it

async def make_item(size):
    return os.urandom(size).hex()

async def randsleep(caller):
    if caller:
        i = random.randint(0,10)
        print(f'{caller} sleeping for {i} seconds.')
        await  asyncio.sleep(i)

async def produce(name, q):
    n = random.randint(1, 10)
    for _ in it.repeat(None, n):
        await randsleep(caller=f'Producer {name}')
        i = await make_item(5)
        t = time.perf_counter()
        await q.put((i, t))
        print(f'Producer {name} added {(i,t)} to queue.')

async def consume(name, q):
    while True:
        await randsleep(f'Consumer {name}')
        i, t = await q.get()
        now = time.perf_counter()
        print(f'Consumer {name} got {(i,t)} in {now-t:0.5f} seconds.')
        q.task_done()

async def main(nprod, ncons):
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(ncons)]
    await asyncio.gather(*producers)
    await q.join()
    for c in consumers:
        c.cancel()

if __name__ == '__main__':
    asyncio.run(main(10,2))
