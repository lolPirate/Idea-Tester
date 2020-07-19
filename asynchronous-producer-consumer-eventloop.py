import asyncio
import time
import os
import random

async def random_work():
    return os.urandom(5).hex()

async def producer(name, q):
    while True:
        i, t = await random_work(), time.perf_counter()
        print(f'Producer {name}: Putting item {(i,t)} in queue.')
        loop.create_task(q.put((i,t)))
        await asyncio.sleep(random.random())

async def consumer(name, q):
    while True:
        i, t = await q.get()
        print(f'Consumer {name} : Task {i} completed in {time.perf_counter() - t:0.5f} seconds.')
        await asyncio.sleep(random.random())

async def main():
    q = asyncio.Queue()
    producer_task = [loop.create_task(producer(name, q)) for name in range(1, 10+1)]
    consumer_task = [loop.create_task(consumer(name, q)) for name in range(1,2+1)]
    await asyncio.wait([*producer_task, *consumer_task])

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.set_debug(1)
    except KeyboardInterrupt as ke:
        print('Program Interrupted! Exiting!')
    except Exception as e:
        print(e)
    finally:
        loop.close()
    