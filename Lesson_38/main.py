from aiohttp import web

from orders import add_order, order_status
from factorial import add_task, get_status


async def create_app():
    app = web.Application()
    app.add_routes([
        web.post('/add_task', add_task),
        web.get('/status', get_status),
        web.post('/add_order', add_order),
        web.get('/order_status', order_status)
    ])

    return app


if __name__ == "__main__":
    app =  create_app()
    web.run_app(app, host='127.0.0.1', port=8000)