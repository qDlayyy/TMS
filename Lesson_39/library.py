from aiohttp import web

books = []
next_book_id = 1

async def create_book(request):
    try:
        data = await request.json()
        global next_book_id

        title = data.get('title')
        author = data.get('author')
        genre = data.get('genre')

        if not title or not author or not genre:
            raise ValueError('Bad request')

        book_data = {
            'id': next_book_id,
            'title': title,
            'author': author,
            'genre': genre
        }

        books.append(book_data)
        next_book_id += 1

        return web.json_response({'detail': 'New book has been created.'}, status=201)


    except Exception as e:
        return web.json_response({'detail': 'Impossible to create the book due to the occurred error.',
                                  'error': e},
                                 status=400)


async def update_book(request):
    try:
        book_id = int(request.match_info['id'])
        data = await request.json()

        for book in books:
            if book['id'] == book_id:
                book['title'] = data.get('title',  book['title'])
                book['author'] = data.get('author',  book['author'])
                book['genre'] = data.get('genre', book['genre'])

                return web.json_response(book, status=200)

        return web.json_response({'detail': 'There is no such books.'}, status=404)

    except Exception as e:
        return web.json_response({'detail': 'Impossible to update the book due to the occurred error.',
                                  'error': e},
                                 status=400)


async def delete_book(request):
    try:
        global books
        book_id = int(request.match_info['id'])

        length = len(books)
        books = [book for book in books if book['id'] != book_id]

        if len(books) < length:
            return web.json_response({'detail': 'The book has been deleted.'}, status=204)

        else:
            return web.json_response({'detail': 'There are no such books.'}, status=404)

    except Exception as e:
        return web.json_response({'detail': 'Impossible to delete the book due to the occurred error.',
                                  'error': e},
                                 status=400)

async def get_books(request):
    try:
        title = request.rel_url.query.get('title')
        author = request.rel_url.query.get('author')
        genre = request.rel_url.query.get('genre')

        all_the_books = books

        if title:
            all_the_books = [book for book in all_the_books if book['title'] == title]

        if author:
            all_the_books = [book for book in all_the_books if book['author'] == author]

        if genre:
            all_the_books = [book for book in all_the_books if book['genre'] == genre]

        return web.json_response(all_the_books, status=200)

    except Exception as e:
        return web.json_response({'detail': 'Impossible to get the book due to the occurred error.',
                                  'error': e},
                                 status=400)
