import os
import jwt
from aiohttp import web

from custom_exception import BookingError
from service import password_to_hash, verify_password, jwt_check, send_email
from datetime import datetime, timedelta

SECRET_KEY = str(os.getenv('SECRET_KEY'))

users_db = []
current_user_id = 1

events_db = []
current_event_id = 1

booked_events_db = []
current_booked_event = 1


async def registration(request):
    try:
        data = await request.json()

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        global users_db
        user = next((user for user in users_db if user['username'] == username), None)

        if user:
            raise BookingError(message='Such user has already been registered.', status=400)

        hashed_password = password_to_hash(password)

        if not username or not email or not password:
            raise BookingError('Invalid data')

        global current_user_id

        user_data = {
            'id': current_user_id,
            'username': username,
            'email': email,
            'password': hashed_password,
            'current_date': datetime.now()
        }

        users_db.append(user_data)
        current_user_id += 1

        return web.json_response({'detail': f'Hello, {username}. Now you can log in!'}, status=201)

    except Exception as e:
        return web.json_response({'detail': 'You cannot be registered due to the occurred exception.',
                                  'error': e},
                                 status=400)


async def login(request):
    try:
        data = await request.json()

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise BookingError('Invalid data')

        user = next((user for user in users_db if user.get('username') == username), None)

        if not user:
            raise BookingError('No users found')

        if not verify_password(password, user['password']):
            raise BookingError('Incorrect data')

        token = jwt.encode({'id': user['id'], 'username': user['username'], 'exp': datetime.utcnow() + timedelta(hours=1)}, SECRET_KEY, algorithm='HS256')

        return web.json_response({'token': token}, status=200)

    except BookingError as e:
        web.json_response({'detail': str(e)}, status=400)

    except Exception as e:
        print(e)
        return web.json_response({'detail': 'Login error due to an exception.',
                                  'error': str(e)},
                                 status=400)


async def create_event(request):
    token = request.headers.get('Authorization')

    if not token:
        return web.json_response({'detail': 'Token is missing'}, status=401)

    token = token.split()[1]

    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    print(payload)
    username = payload['username']

    try:
        data = await request.json()

        event_name = data.get('name')
        event_desc = data.get('description')
        event_date = data.get('date')
        event_place = data.get('place')

        if not event_name or not event_desc or not event_date or  not event_place:
            raise BookingError('Invalid data')

        global current_event_id

        event_data = {
            'id': current_event_id,
            'name': event_name,
            'description': event_desc,
            'place': event_place,
            'date': event_date,
            'creator': username
        }

        events_db.append(event_data)
        current_event_id += 1

        return web.json_response(event_data, status=201)

    except BookingError as e:
        return web.json_response({'detail': 'Impossible to create new event due to an exception.',
                                  'error': str(e)},
                                 status=400)

    except Exception as e:
        return web.json_response(
            {'detail': 'Impossible to create new event due to an exception.',
             'error': str(e)},
            status=400)


async def get_events(request):
    try:
        target_date = request.rel_url.query.get('date')
        target_place = request.rel_url.query.get('place')

        filtered_events = events_db

        if target_date:
            filtered_events = [event for event in filtered_events if event['date'] == target_date]

        if target_place:
            filtered_events = [event for event in filtered_events if event['place'] == target_place]

        return web.json_response(filtered_events, status=200)

    except Exception as e:
        return web.json_response(
            {'detail': 'Impossible to get events due to an exception.',
             'error': str(e)},
            status=400)


async def book_event(request):
    try:
        jwt_payload = jwt_check(request)
        event_id = int(request.match_info['id'])
        event = next((event for event in events_db if event['id'] == event_id), None)

        if not event:
            raise BookingError(message='No events found', status=404)

        global current_booked_event

        booked_data = {
            'id': current_booked_event,
            'event': event,
            'user_id': jwt_payload.get('id'),
        }

        user = next((user for user in users_db if user['id'] == jwt_payload['id']), None)
        send_email(username=user['username'], email=user['email'], event=event)

        booked_events_db.append(booked_data)
        current_booked_event += 1

        return web.json_response({'detail': f'Event {event["name"]} has been booked successfully'}, status=200)

    except BookingError as e:
        return web.json_response(
            {'detail': 'Impossible to book an event due to an exception.',
             'error': str(e)},
            status=e.status)

    except Exception as e:
        return web.json_response(
            {'detail': 'Impossible to book an event due to an exception.',
             'error': str(e)},
            status=400)


async def get_booked_events(request):
    try:
        jwt_payload = jwt_check(request)
        filtered_events = [event for event in booked_events_db if event['user_id'] == jwt_payload['id']]

        if not filtered_events:
            return web.json_response({'detail': 'You haven\'t booked any events yet.'}, status=200)

        return web.json_response(filtered_events, status=200)

    except BookingError as e:
        return web.json_response(
            {'detail': 'Impossible to get booked events due to an exception.',
             'error': str(e)},
            status=e.status)

    except Exception as e:
        return web.json_response(
            {'detail': 'Impossible to get booked events due to an exception.',
             'error': str(e)},
            status=400)


async def delete_booked_event(request):
    try:
        jwt_payload = jwt_check(request)
        event_id = int(request.match_info['id'])

        event = next((event for event in booked_events_db if event['id'] == event_id), None)

        if not event:
            raise BookingError('No events found', status=404)

        if not event['user_id'] == jwt_payload['id']:
            raise BookingError('You cannot cancel this event', status=403)

        length_before_delete = len(booked_events_db)
        booked_events_db.remove(event)

        if not length_before_delete < len(booked_events_db):
            raise BookingError(message='Something went wrong, cannot cancel event', status=400)

        return web.json_response({'detail': f'Event has been canceled.'}, status=204)

    except BookingError as e:
        return web.json_response(
            {'detail': 'Impossible to cancel booked event due to an exception.',
             'error': str(e)},
            status=e.status)

    except Exception as e:
        return web.json_response(
            {'detail': 'Impossible to cancel an event due to an exception.',
             'error': str(e)},
            status=400)

