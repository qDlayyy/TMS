import asyncio
from random import randint
from typing import Optional

from aiohttp import web

factorial_queue = asyncio.Queue()
factorial_workers_count = 0

async def factorial(n):
    if n < 1:
        return 1

    result = 1
    for number in range(1, n + 1):
        result *= number

    return result


async def worker(worker_id):
    while True:
        task = await factorial_queue.get()
        print(f'Factorial Worker #{worker_id} has started task: factorial({task}).')
        result = await factorial(task)
        await asyncio.sleep(randint(2,8))
        print(f'Factorial Worker #{worker_id} has finished task: factorial({task}) = {result}')

        factorial_queue.task_done()


async def worker_creation():
    worker_needed = 2
    global factorial_workers_count
    factorial_workers_count = worker_needed

    for worker_id in range(1, worker_needed + 1):
        asyncio.create_task(worker(worker_id))
        print(f'New Factorial Worker #{worker_id} has been created.')


async def add_task(request):
    try:
        data = await request.json()
        number = data.get('number')
        list_of_numbers = data.get('numbers')

        if not number and not list_of_numbers:
            raise (ValueError('No Provided data.'))

        if not isinstance(number, Optional[int]) or isinstance(number, int) and number < 0:
            raise(ValueError('Provided data does not contain a number or the number is negative.'))

        if not isinstance(list_of_numbers, Optional[list]):
            raise (ValueError('Provided data does not contain a list of numbers'))

        if factorial_workers_count == 0:
            await worker_creation()

        wrong_data_flag = await queue_adder(number, list_of_numbers)

        if not wrong_data_flag:
            return web.json_response({'detail': f'New task/tasks \'Factorial()\' have been successfully added.'}, status=200)

        else:
            return web.json_response({'detail': f'New task/tasks \'Factorial()\' have been successfully added with filtered data among list of numbers.'},
                                     status=200)

    except Exception as e:
        return web.json_response({'detail': 'An error has occurred.',
                                  'error': e},
                                 status=400)


async def queue_adder(*args, **kwargs):
    list_data_controller = True
    for arg in args:
        if isinstance(arg, int):
            await factorial_queue.put(arg)

        elif isinstance(arg, list):
            for number in arg:
                if isinstance(number, int):
                    await factorial_queue.put(number)

                else:
                    list_data_controller = False

    return list_data_controller


async def get_status(request):
    current_queue_status = factorial_queue.qsize()

    return web.json_response({'tasks': current_queue_status}, status=200)
