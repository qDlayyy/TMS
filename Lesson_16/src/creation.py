from src.common import get_all_names_info, get_all_ids, date_formation
from src.database import SessionLocal, Places, Events, Tickets
from src.service import InputCheck, ServiceException


def adding_data():
    list_of_categories = ['\n1. Add place', '2. Add event', '3. Add ticket', '4. Quit adding']
    try:
        list(map(lambda item: print(item), list_of_categories))
        choice = input('\nChoose the category you want to add: ')
        choice = InputCheck.within(target_number=choice, target_list=list_of_categories)
        match choice:
            case 1:
                add_process(category='place')
            case 2:
                add_process(category='event')
            case 3:
                add_process(category='ticket')
            case 4:
                raise ServiceException('\nAdding has been canceled.')

    except Exception as e:
        print(e)


def add_process(category):
    if category == 'place':
        try:
            target_string = input('\nThe name of the place: ')
            name = InputCheck.nes(target_string=target_string)

            target_string = input('\nThe address of the place: ')
            address = InputCheck.nes(target_string=target_string)

            description = input('\nThe description of the place: ')

            with SessionLocal() as session:
                add_place(session=session, name=name, address=address, description=description)
            print('\n~ The place has been added.')

        except Exception as e:
            print(e)

    elif category == 'event':
        try:
            target_string = input('\nThe name of the event: ')
            event_name = InputCheck.nes(target_string=target_string)

            list_of_info = get_all_names_info(table_name=Places)
            print()
            for info in list_of_info:
                print(f'{info[0]}. {info[1]}.')
            print('Enter q to cancel event add.')
            point = input('\nThe location of the event: ')

            if point != 'q':
                point = InputCheck.inc(point)
                if point not in get_all_ids(table_name=Places):
                    raise ServiceException('\n### There is no such place id. ###')
            else:
                raise ServiceException('\nEvent add has been cancelled.')

            date_object = date_formation()

            description = input('\nThe description of the event: ')

            with SessionLocal() as session:
                add_event(session=session, name=event_name, place_id=point, date=date_object, description=description)
            print('\n~ The event has been added.')
        except Exception as e:
            print(e)

    elif category == 'ticket':
        try:
            target_place = input('\nThe seat: ')
            place = InputCheck.nes(target_string=target_place)

            list_of_event_info = get_all_names_info(table_name=Events)
            print()
            for info in list_of_event_info:
                print(f'{info[0]}. {info[1]}.')
            print('Enter q to cancel ticket add.')

            point = input('\nThe location of the event: ')
            if point != 'q':
                point = InputCheck.inc(point)
                if point not in get_all_ids(table_name=Events):
                    raise ServiceException('\n### There is no such event id. ###')
            else:
                raise ServiceException('\nTicket add has been cancelled.')

            target_price = input('\nThe price of the ticket (BYN): ')
            price = InputCheck.fnc(target_number=target_price)

            with SessionLocal() as session:
                add_ticket(session=session, place=place, event_id=point, price=price)
            print('\n~ The ticket has been added.')
        except Exception as e:
            print(e)

    else:
        raise ServiceException('\n### Unexpected category. ###')


def add_place(session, name, address, description):
    place = Places(name=name, address=address, description=description)
    session.add(place)
    session.commit()


def add_event(session, name, place_id, date, description):
    event = Events(name=name, place_id=place_id, date=date, description=description)
    session.add(event)
    session.commit()


def add_ticket(session, place, event_id, price):
    ticket = Tickets(place=place, event_id=event_id, price=price)
    session.add(ticket)
    session.commit()