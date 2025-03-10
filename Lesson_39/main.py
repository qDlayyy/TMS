from aiohttp import web
from library import create_book, get_books, update_book, delete_book
from booking import registration, login, create_event, get_events, book_event, get_booked_events, delete_booked_event

from dotenv import load_dotenv
load_dotenv()

async def create_app():
    app = web.Application()
    app.add_routes([
        web.post('/books', create_book),
        web.get('/books', get_books),
        web.put('/books/{id}', update_book),
        web.delete('/books/{id}', delete_book),
        web.post('/registration', registration),
        web.post('/login', login),
        web.post('/events', create_event),
        web.get('/events', get_events),
        web.post('/book/{id}', book_event),
        web.get('/book', get_booked_events),
        web.delete('/book/{id}', delete_booked_event)
    ])

    return app

if __name__ == "__main__":
    web.run_app(create_app(), port=8000)