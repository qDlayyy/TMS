from sqlalchemy import or_
from src.database import SessionLocal, Places, Events, Tickets
from src.service import InputCheck, ServiceException


def searching():
    try:
        query = input('\nWhat you are looking for? The result will show all possible matches in all data: ')
        query = InputCheck.nes(target_string=query).lower()

        with SessionLocal() as session:
            results = deep_searching(session=session, target_query=query)
        searched_results_recognition(session=session, results=results)
    except Exception as e:
        print(e)


def deep_searching(session, target_query):
    results = {}
    models = [Places, Events, Tickets]
    for model in models:
        columns = [column.name for column in model.__table__.columns]
        query = session.query(model)

        conditions = []
        for column_name in columns:
            column = getattr(model, column_name)
            conditions.append(column.like(f'%{target_query}%'))

        results[model.__tablename__] = query.filter(or_(*conditions)).all()

    return results


def searching_for_places_by_place_id(session, place_id, item):
    place = session.query(Places).filter(Places.id == place_id).first()

    if place:
        place = place.__dict__
    else:
        place_name_plug = 'The place has been deleted from the database'

    if item:
        return(
            {
                'place_name': place['name'] if place else place_name_plug,
                'event_id': item['id'],
                'event_name': item['name'],
                'event_date': item['date'],
                'event_description': item['description'],
            }
        )
    else:
        return(
            {
                'place_name': place['name'] if place else place_name_plug,
            }
        )


def searching_for_events_by_event_id(session, event_id, item):
    event = session.query(Events).filter(Events.id == event_id).first()

    if event:
        event = event.__dict__
    else:
        event_name_plug = 'This event has been cancelled'
        event_date_plug = 'No Data'
        event_description_plug = 'No Data'
        place_id_plug = None

    if item:
        return(
            {
                'event_name': event['name'] if event else event_name_plug,
                'event_date': event['date'] if event else event_date_plug,
                'event_description': event['description'] if event else event_description_plug,
                'place_id': event['place_id'] if event else place_id_plug,
                'seat': item['place'],
                'price': item['price'],
                'booking': item['booking'],
            }
        )


def searched_results_recognition(session, results):
    for table, items in results.items():
        if items:
            print(f"\n\n~ All matches found in model {table}: ")
        else:
            print(f'\n\n~ No matches found in model {table}.')

        if table == 'places':
            for item in items:
                item = item.__dict__
                print(f'\n\tID: {item["id"]}',
                      f'\tName: {item["name"]}',
                      f'\tAddress: {item["address"]}',
                      f'\tDescription: {item["description"] if item["description"] else "No description for that place."}',
                      sep='\n')
        elif table == 'events':
            results = []
            for item in items:
                item = item.__dict__
                place_id = item["place_id"]
                results.append(searching_for_places_by_place_id(session=session, place_id=place_id, item=item))

            for result in results:
                print(
                    f'\n\tID: {result["event_id"]}',
                    f'\tName: {result["event_name"]}',
                    f'\tDate: {result["event_date"]}',
                    f'\tPlace: {result["place_name"]}',
                    f'\tDescription: {result["event_description"] if result["event_description"] else "No description for that event."}',
                    sep='\n'
                )
        elif table == 'tickets':
            results = []
            for item in items:
                item = item.__dict__
                event_id = item["event_id"]
                dict_of_ticket_and_event_id = searching_for_events_by_event_id(session=session, event_id=event_id, item=item)
                place_id = dict_of_ticket_and_event_id['place_id']
                if place_id:
                    dict_of_event_and_place = searching_for_places_by_place_id(session=session, place_id=place_id, item=None)
                else:
                    dict_of_event_and_place = {}
                dict_of_full_ticket_info = dict_of_ticket_and_event_id | dict_of_event_and_place

                results.append(dict_of_full_ticket_info)

            for result in results:
                booking_status = result["booking"]
                print(
                    f'\n\tEvent: {result["event_name"]}',
                    f'\tPlace: {result["place_name"] if result.get("place_name") else "No Data"}',
                    f'\tDate: {result["event_date"]}',
                    f'\tDescription: {result["event_description"] if result["event_description"] else "No description for that event."}',
                    f'\tSeat: {result["seat"]}',
                    f'\tPrice: {result["price"]}',
                    f'\tBooking: {booking_status if booking_status == "Available" else f"Booked by {booking_status}"}',
                    sep='\n'
                )
        else:
            raise ServiceException('\n### Warning. Results cannot be shown. ###\n')