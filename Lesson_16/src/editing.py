from src.common import get_all_names_info, get_all_places, get_all_ids, get_full_info_by_id, date_formation
from src.database import Places, Events, Tickets, SessionLocal
from src.service import ServiceException, InputCheck


def editing_determination(table_flag):
    if table_flag == 'place':
        text_plug = table_flag
        table_name = Places
    elif table_flag == 'event':
        text_plug = table_flag
        table_name = Events
    elif table_flag == 'ticket':
        text_plug = table_flag
        table_name = Tickets
    else:
        raise ServiceException('\n### Invalid table name. ###')

    if table_name != Tickets:
        list_of_info = get_all_names_info(table_name=table_name)
    else:
        list_of_info = get_all_places(table_name=table_name)

    for info in list_of_info:
        print(f'{info[0]}. {info[1]}')

    table_choice = input(f'\nChoose the {text_plug} you want to edit: ')
    table_choice = InputCheck.inc(target_number=table_choice)

    if table_choice not in get_all_ids(table_name=table_name):
        raise ServiceException(f'\n### There is no such {text_plug} id. ###')

    dict_of_info = get_full_info_by_id(table_name=table_name, item_id=table_choice)
    dict_keys = list(dict_of_info.keys())

    for parameter_id, parameter in enumerate(dict_keys):
        print(f'{parameter_id + 1}. {dict_of_info[parameter]}')
    param_choice = input('\nChoose the parameter you want to edit: ')
    param_choice = InputCheck.within(target_number=param_choice, target_list=dict_keys)
    parameter = list(dict_of_info.keys())[param_choice - 1]

    if parameter == 'id':
        raise ServiceException(f'\n### You cannot change {text_plug} id. ###')
    elif table_flag == 'event' and parameter == 'date':
        new_parameter = date_formation()
    elif table_flag == 'event' and parameter == 'place_id':
        list_of_info = get_all_names_info(table_name=Places)
        for info in list_of_info:
            print(f'{info[0]}. {info[1]}')
        place_choice = input('\nChoose the place you want to edit: ')
        place_choice = InputCheck.inc(target_number=place_choice)
        if place_choice not in get_all_ids(table_name=Places):
            raise ServiceException('\n### There is no such place id. ###')
        new_parameter = place_choice
    elif table_flag == 'ticket' and parameter == 'event_id':
        list_of_info = get_all_names_info(table_name=Events)
        for info in list_of_info:
            print(f'{info[0]}. {info[1]}')
        event_choice = input('\nChoose the event you want to edit: ')
        event_choice = InputCheck.inc(target_number=event_choice)
        if event_choice not in get_all_ids(table_name=Events):
            raise ServiceException('\n### There is no such place id. ###')
        new_parameter = event_choice
    elif table_flag == 'ticket' and parameter == 'price':
        price = input('\nEnter new price: ')
        new_parameter = InputCheck.fnc(target_number=price)
    else:
        new_parameter = input('\nEnter new data: ')
        new_parameter = InputCheck.nes(target_string=new_parameter)

    with SessionLocal() as session:
        edit_data(session=session, table=table_name, item_id=table_choice, parameter=parameter, new_data=new_parameter)

    print(f'\n~ The {text_plug} has been updated.')


def edit_data(session, table, item_id, parameter, new_data):
    data = session.query(table).filter(table.id == item_id).first()

    if hasattr(data, parameter):
        setattr(data, parameter, new_data)
        session.commit()
    else:
        raise ServiceException('\n### Data cannot be changed. ###')


def editing_data():
    list_of_categories = ['\n1. Edit place', '2. Edit event', '3. Edit ticket', '4. Quit editing']
    try:
        list(map(lambda item: print(item), list_of_categories))
        choice = input('\nChoose the category you want to edit: ')
        choice = InputCheck.within(target_number=choice, target_list=list_of_categories)
        match choice:
            case 1:
                editing_determination(table_flag='place')

            case 2:
                editing_determination(table_flag='event')

            case 3:
                editing_determination(table_flag='ticket')

            case 4:
                raise ServiceException('\nEditing data has been cancelled. \n')
    except Exception as e:
        print(e)