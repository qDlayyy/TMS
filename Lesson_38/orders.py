import asyncio
from random import randint

from aiohttp import web

order_queue = asyncio.Queue()
order_worker_count = 0

async def price_formation(obj):
    k = 1.4
    amount = obj.get('amount')
    price_per_unit = obj.get('price')
    sale_percentage = obj.get('sale')

    if not obj.get('title') or not amount or not price_per_unit or (sale_percentage and sale_percentage > 100):
        raise ValueError('Not enough data.')

    full_price = price_per_unit * k * amount

    if sale_percentage:
        full_price *= sale_percentage / 100

    full_price = round(full_price, 2)

    obj['full_price'] = full_price


    return full_price


async def add_order(request):
    try:
        data = await request.json()
        await order_queue.put(data)

        if order_worker_count == 0:
            await worker_creation()

        return web.json_response({'detail': f'New order \'{data.get("title")}\' has been added.'}, status=200)

    except Exception as e:
        return web.json_response({'detail': 'An error has occurred.',
                                  'error': e},
                                 status=400)


async def worker(worker_id):
    while True:
        task = await order_queue.get()
        print(f'Order Worker #{worker_id} has started task: \'Price Formation\' for {task.get("title")}.')
        result = await price_formation(task)

        await asyncio.sleep(randint(10, 20))

        print(f'Order Worker #{worker_id} has finished task: \'Price Formation\' for {task.get("title")}. Final price is {result} .')

        order_queue.task_done()


async def worker_creation():
    worker_needed = 3
    global order_worker_count
    order_worker_count= worker_needed
    for worker_id in range(1, worker_needed + 1):
        asyncio.create_task(worker(worker_id))
        print(f'New Order Worker #{worker_id} has been created.')


async def order_status(request):
    current_order_status = order_queue.qsize()

    return web.json_response({'current_order_status': current_order_status}, status=200)
