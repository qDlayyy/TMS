from src.menu_classes import T1SodaFlavour, T2Math, T3Car, T4Sphere, T5String, Exit
from src.service import InputCheck


class Menu:
    def __init__(self, correct_input, items):
        self._input_check = correct_input
        self._items = items

    def run(self):
        while True:
            list(map(lambda point: print(point['point']), self._items))
            try:
                choice = input('\nChoose the menu point: ')
                choice = self._input_check.menu_point_validation(choice=choice, menu_length=len(self._items))
                items[choice - 1]['action'].execute()
            except Exception as exception:
                print(exception)


if __name__ == '__main__':

    correct_input = InputCheck()
    items = [
        {'point': '\n1. Soda Flavour;', 'action': T1SodaFlavour(correct_input=correct_input)},
        {'point': '2. Math', 'action': T2Math(correct_input=correct_input)},
        {'point': '3. Car', 'action': T3Car(correct_input=correct_input)},
        {'point': '4. Sphere', 'action': T4Sphere(correct_input=correct_input)},
        {'point': '5. Super String', 'action': T5String(correct_input=correct_input)},
        {'point': '6. Exit', 'action': Exit()}
    ]
    menu = Menu(correct_input=correct_input, items=items)
    menu.run()