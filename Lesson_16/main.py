from src.booking import ticket_booking
from src.creation import adding_data
from src.deletion import deleting_data
from src.editing import editing_data
from src.searching import searching
from src.service import InputCheck


def main_loop():
    list_of_items = ['\n1. Add Data', '2. Delete Data', '3. Edit Data', '4. Searching', '5. Book Tickets', '6. Quit']
    while True:
        list(map(lambda item: print(item), list_of_items))
        try:
            point = input('\nChoose the menu point: ')
            point = InputCheck.within(target_number=point, target_list=list_of_items)

            match point:
                case 1:
                    adding_data()
                case 2:
                    deleting_data()
                case 3:
                    editing_data()
                case 4:
                    searching()
                case 5:
                    ticket_booking()
                case 6:
                    return False

        except Exception as e:
            print(e)


if __name__ == '__main__':
    main_loop()