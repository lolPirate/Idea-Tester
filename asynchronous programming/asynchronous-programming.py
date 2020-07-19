import asyncio

def logger(func):
    '''
    Logger function to give verbose of logging procedure.
    '''
    async def logging_func(*args, **kwargs):
        '''
        Modified find_factorial funcction to enable logging.
        Note: We wait on the func as find_factorial itself waits
        '''
        print(f'Running factorial for n = {args[0]}')
        res = await func(*args)
        print(f'Completed running for n = {args[0]}')
        return res
    return logging_func
    
@logger
async def find_factorial(n):
    fact = 1
    for i in range(1, n+1):
        fact *= i
        await asyncio.sleep(0.001)
    print(f'{n}! = {fact}')
    return fact

async def main(*args):
    routines = []
    for i in args[0]:
        routine = loop.create_task(find_factorial(i)) # Creates a bunch of co-routines 
        routines.append(routine) # appends all the co-routines to a list
    await asyncio.wait([*routines]) #awaits each co-routine
    return routines
    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()  # main event loop
    #loop.set_debug(1)  # use for debugging
    try:
        factorial = [25, 600, 0, 400, 6, 120, 3, 1, 9, 100]
        fact = loop.run_until_complete(main(factorial))  # running our main asynchronous function
        results = [i.result() for i in fact]
        print(results)
    except Exception as e:
        print(e)
    finally:
        loop.close()
