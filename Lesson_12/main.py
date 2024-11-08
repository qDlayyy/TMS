
from src.service import InputCheck, ServiceException
from src.classes import Warehouse, BeeElephant, Bus

class T1ProductsAndWarehouse:
    def __init__(self):
        self._item = ['\n1. Product by index', '2. Product by name', '3. Sort by name', '4. Sort by store name', '5. Sort by price',
                      '6. Product sum', '7. Full products info', '8. Exit Warehouse&Products']

    def _inner_menu(self):
        list(map(lambda item: print(item), self._item))


    @staticmethod
    def warehouse_determination():
        while True:
            try:
                number_of_products = input('\nHow many products do you want to generate? ')
                number_of_products = InputCheck.inc(target_number=number_of_products)
                number_of_products = InputCheck.nbtc(target_number=number_of_products, border_nums_tuple=(1,100))
                return Warehouse.generate_random_warehouse(number_of_products=number_of_products)

            except Exception as e:
                print(e)


    def execute(self):
        warehouse = self.warehouse_determination()
        while True:
            self._inner_menu()
            try:
                choice = input('\nChoose the Product&Warehouse point: ')
                choice = InputCheck.mic(choice=choice, menu_list=self._item)

                match choice:
                    case 1:
                        list_of_products = warehouse.show_products()
                        while True:
                            try:
                               choice = input('\nChoose the product id: ')
                               choice = InputCheck.mic(choice=choice, menu_list=list_of_products)
                               found_item = warehouse[choice - 1]
                               warehouse.show_info(found_product=found_item)
                               break
                            except Exception as e:
                                print(e)

                    case 2:
                        target_name = input('\nWhat name are you looking for? ')
                        target_name = InputCheck.nes(string=target_name)
                        found_products = warehouse.find_products(name=target_name)
                        if not found_products:
                            raise ServiceException('\n### Warning. No such product found. ###\n')
                        else:
                            for product in found_products:
                                warehouse.show_info(found_product=product)

                    case 3:
                        warehouse.name_sort()
                        warehouse.show_full_products()

                    case 4:
                        warehouse.store_sort()
                        warehouse.show_full_products()
                    case 5:
                        warehouse.price_sort()
                        warehouse.show_full_products()
                    case 6:
                        list_of_products = warehouse.show_products()
                        while True:
                            try:
                                chosen_items = input("\nChoose all products' IDs using SPACE between them (2 3 4 1 2). Incorrect numbers will be kicked: ").strip().split(' ')
                                chosen_items = list(map(lambda product: int(product), chosen_items))
                                chosen_items = InputCheck.list_of_nums_within_the_list(list_of_numbers=chosen_items, menu_list=list_of_products)
                                print(chosen_items)
                                list_of_products, result = warehouse.products_sum_by_ids(list_of_ids=chosen_items)
                                if list_of_products:
                                    print(f'\n~ List of products you\'ve chosen: {", ".join(list_of_products)}',
                                          f'\tSum price: {result} BYN',
                                          sep='\n')
                                else:
                                    print('\n~ None of the products you\'ve chosen exist.')
                                break
                            except ValueError:
                                print('\n### Warning. There is not a number in your list of product IDs. Try again. ###\n')
                            except Exception as e:
                                print(e)

                    case 7:
                        warehouse.show_full_products()

                    case 8:
                        return False


            except Exception as exception:
                print(exception)


class T2BeeElephant:
    def __init__(self):
        self._items = ['\n1. Try to fly', '2. Trumpet', '3. Feed the BeeElephant', '4. BeeElephant status',
                       '5. Exit BeeElephant']
        self._input_texts = ['\nHow big is Bee part (0, 100): ', '\nWhat is the size of Elephant part (0, 100): ']
        self._range_tuple = (0, 100)


    def _inner_menu(self):
        list(map(lambda item: print(item), self._items))


    def bee_elephant_determination(self):
        while True:
            try:
                bee_part, elephant_part = InputCheck.multiple_int_inputs_range_check(list_of_input_texts=self._input_texts,
                                                                                     range_tuple=self._range_tuple)
                return BeeElephant(bee_part=bee_part, elephant_part=elephant_part)

            except Exception as e:
                print(e)


    def execute(self):
        bee_elephant = self.bee_elephant_determination()
        while True:
            self._inner_menu()
            try:
                choice = input('\nChoose the BeeElephant point: ')
                choice = InputCheck.mic(choice=choice, menu_list=self._items)

                match choice:
                    case 1:
                        is_flyable = bee_elephant.fly()
                        if is_flyable:
                            print('\n~ The BeeElephant is flying.')
                        else:
                            print('\n~ The BeeElephant is too heavy for flying.')
                    case 2:
                        trumpet = bee_elephant.trumpet()
                        print(f'\n~ {trumpet}')
                    case 3:
                        try:
                            meal = input('\nChoose the meal for BeeElephant. Usually it eats either nectar or grass: ')
                            value = input('\nWhat is the value of the meal? Remember the BeeElephant cannot eat more than 100: ')
                            value = InputCheck.inc(target_number=value)
                            value = InputCheck.nbtc(target_number=value, border_nums_tuple=(0,100))
                            bee_elephant.eat(meal=meal, value=value)
                        except Exception as e:
                            print(e)
                    case 4:
                        bee_elephant.show_bee_elephant()
                    case 5:
                        return False
            except Exception as e:
                print(e)


class T3Bus:
    def __init__(self):
        self._items = ['\n1. Boarding & Disembarkation', '2. Speed change', '3. Bus status', '4. Exit Bus']

    def _inner_menu(self):
        list(map(lambda item: print(item), self._items))

    @staticmethod
    def bus_determination():
        bus = Bus()
        bus.engine_engage()
        return bus

    def execute(self):
        bus = self.bus_determination()
        while True:
            self._inner_menu()
            try:
                choice = input('\nChoose the Bus point: ')
                choice = InputCheck.mic(choice=choice, menu_list=self._items)
                match choice:
                    case 1:
                        try:
                            string_of_passengers_out = input(
                                '\nList the passengers\' surnames to leave the bus. Use SPACE to determine them or leave it empty: ')
                            string_of_passengers_out = InputCheck.string_separator_check(permissible_separators=[' '],
                                                                                         target_string=string_of_passengers_out)
                            string_of_passengers_in = input('\nList the passengers\' surnames to enter the bus. Use SPACE to determine them or leave it empty: ')
                            string_of_passengers_in = InputCheck.string_separator_check(permissible_separators=[' '],
                                                                                        target_string=string_of_passengers_in)

                            list_of_passengers_out = string_of_passengers_out.split(' ')
                            list_of_passengers_in = string_of_passengers_in.split(' ')
                            bus.bus_stop(list_out=list_of_passengers_out, list_in=list_of_passengers_in)
                        except Exception as e:
                            # print('\n### Warning. Something went wrong with the doors. Impossible to board or disembark passengers. ###')
                            print(e)
                    case 2:
                        while True:
                            try:
                                target_speed = input('\nBy how many km/h should the bus accelerate (x) or decelerate (-x): ')
                                speed = InputCheck.inc(target_number=target_speed)
                                bus.speed_changer(speed=speed)
                                break
                            except Exception as e:
                                print(e)
                    case 3:
                        bus.bus_status()
                    case 4:
                        bus.engine_muffle()
                        return False

            except Exception as e:
                print(e)


class Exit:
    def __init__(self):
        pass

    @staticmethod
    def execute():
        exit()


class Menu:
    def __init__(self):
        self._items = [
            {'point': '\n1. Products & Warehouse', 'action': T1ProductsAndWarehouse()},
            {'point': '2. BeeElephant', 'action': T2BeeElephant()},
            {'point': '3. Bus', 'action': T3Bus()},
            {'point': '4. Exit', 'action': Exit()}
        ]

    def _menu_show(self):
        list(map(lambda item: print(item['point']), self._items))

    def run(self):
        while True:
            self._menu_show()
            try:
                choice = input('\nChoose the Menu point: ')
                choice = InputCheck.mic(choice=choice, menu_list=self._items)

                self._items[choice - 1]['action'].execute()

            except Exception as e:
                print(e)

if __name__ == '__main__':
    # T1ProductsAndWarehouse().execute()
    # T2BeeElephant().execute()
    # T3Bus().execute()
    menu = Menu()
    menu.run()