from src.common import get_all_names_info, get_all_places, get_all_ids
from src.database import Places, Events, Tickets, SessionLocal
from src.service import ServiceException, InputCheck


def deleting_data():
    list_of_categories = ['\n1. Delete place', '2. Delete event', '3. Delete ticket', '4. Quit deleting']
    try:
        list(map(lambda item: print(item), list_of_categories))
        choice = input('\nChoose the category you want to delete: ')
        choice = InputCheck.within(target_number=choice, target_list=list_of_categories)
        match choice:
            case 1:
                deletion_process(category='place')
            case 2:
                deletion_process(category='event')
            case 3:
                deletion_process(category='ticket')
            case 4:
                raise ServiceException('\nAdding has been canceled.')

    except Exception as e:
        print(e)


def deletion_process(category):
    if category == 'place':
        table = Places
        text_plug = category
    elif category == 'event':
        table = Events
        text_plug = category
    elif category == 'ticket':
        table = Tickets
        text_plug = category
    else:
        raise ServiceException('\n### Unexpected category. ###')

    if category != 'ticket':
        list_of_info = get_all_names_info(table_name=table)
    else:
        list_of_info = get_all_places(table_name=table)

    for info in list_of_info:
        print(f'{info[0]}. {info[1]}')
    point = input('\nWhat point should be deleted: ')
    point = InputCheck.inc(point)

    if point not in get_all_ids(table_name=table):
        raise ServiceException(f'\n### There is no such {text_plug} id. ###')

    with SessionLocal() as session:
        delete_data(session=session, table=table, place_id=point)
        print(f'\n~ The {text_plug} has been deleted.')


def delete_data(session, table, place_id):
    session.query(table).filter(table.id == place_id).delete()
    session.commit()