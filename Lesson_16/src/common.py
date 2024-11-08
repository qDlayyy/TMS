from datetime import datetime
from src.database import SessionLocal
from src.service import InputCheck


def date_formation():
    while True:
        try:
            target_year = input('\nThe year of the event: ')
            year = InputCheck.inc(target_year)

            target_month = input('\nThe month of the event(1-12): ')
            month = InputCheck.inc(target_month)

            day = input('\nThe day of the event(1-31): ')
            day = InputCheck.inc(day)

            date_object = datetime.strptime(f'{year}-{month}-{day}', "%Y-%m-%d").date()

            return date_object

        except ValueError as e:
            print('\n### Warning. Unexpected date format. ###')

        except Exception as e:
            print(e)


def get_all_names_info(table_name):
    with SessionLocal() as session:
        try:
            info = session.query(table_name.id, table_name.name).all()
        except Exception as e:
            print(e)
    return info


def get_all_places(table_name):
    with SessionLocal() as session:
        try:
            info = session.query(table_name.id, table_name.place).all()
        except Exception as e:
            print(e)
    return info


def get_full_info_by_id(table_name, item_id):
    with SessionLocal() as session:
        try:
            item = session.query(table_name).filter(table_name.id == item_id).first()
            if item:
                dict_of_info = item.info()
                return dict_of_info
        except Exception as e:
            print(e)


def get_all_ids(table_name):
    with SessionLocal() as session:
        try:
            ids = session.query(table_name.id).all()
            list_of_ids = [item_id[0] for item_id in ids]
        except Exception as e:
            print(e)
    return list_of_ids


def get_all_ids_where(table_name, column_name, column_value):
    with SessionLocal() as session:
        try:
            column = getattr(table_name, column_name)
            values = session.query(table_name.id).filter(column == column_value)
            list_of_values = [value[0] for value in values]
            return list_of_values
        except Exception as e:
            print(e)