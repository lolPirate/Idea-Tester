import asyncio
import time
import os
import random

async def random_work():
    i = os.urandom(5).hex()
    t = time.perf_counter()
    with open('producer.txt', mode='a+') as f:
        await asyncio.sleep(random.random())
        data = f'Created work <{i}> at {t:>1.3f} seconds.\n'
        f.write(data)
    return i, t

async def do_random_work(i, t):
    completed_time = time.perf_counter() - t
    with open('consumer.txt', mode='a+') as f:
        await asyncio.sleep(random.random())
        data = f'Completed work <{i}> at {time.perf_counter():>1.3f} seconds.\n'
        f.write(data)
    return completed_time


async def producer(name, q):
    while True:
        i, t = await random_work()
        print(f'Producer {name:>2}: Putting item {i} at time {t} in queue.')
        loop.create_task(q.put((i,t)))
        

async def consumer(name, q):
    while True:
        i, t = await q.get()
        work = await do_random_work(i,t)
        print(f'Consumer {name:>2}: Task {i} completed in {work:>1.3f} seconds.')

async def main():
    q = asyncio.Queue()
    print('Spawnig Producers')
    producer_task = [loop.create_task(producer(name, q)) for name in range(1, 10+1)]
    print('Spawnig Consumers')
    consumer_task = [loop.create_task(consumer(name, q)) for name in range(1,9+1)]
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
    