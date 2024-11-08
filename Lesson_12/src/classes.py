import random
import string
from src.service import ServiceException


class Product:
    def __init__(self, name, store_name, price):
        self._name = name
        self._store_name = store_name
        self._price = price


    def __add__(self, other):
        if isinstance(other, Product):
            name = f'{self._name} & {other._name}'
            new_price = self._price + other._price
            return Product(name, self._store_name, new_price)
        else:
            raise ServiceException('\n### Warning. You cannot count sum. ###\n')


    def show_info(self):
        print(f'\n~ Product name: {self._name}',
              f'  Store name: {self._store_name}',
              f'  Price: {self._price}',
              sep='\n')


    @property
    def name(self):
        return self._name


    @property
    def store_name(self):
        return self._store_name

    @property
    def price(self):
        return self._price


class Warehouse:
    def __init__(self, list_of_products):
        self._products: list[Product] = list_of_products


    def __getitem__(self, item_id):
        return self._products[item_id]


    def find_product(self, name):
        for product in self._products:
            if product.name.lower() == name.strip().lower():
                return product
        return None

    def find_products(self, name):
        list_of_found_products = []
        for product in self._products:
            if product.name.lower() == name.strip().lower():
                list_of_found_products.append(product)

        return list_of_found_products if list_of_found_products else None


    def sum_products(self, product_one_id, product_two_id):
        try:
            product_one = self.find_product(product_one_id)
            product_two = self.find_product(product_two_id)
        except:
            raise ServiceException('\n### Warning. Product ID exception. ###\n')

        new_product = product_one + product_two
        return new_product


    def name_sort(self):
        self._products.sort(key=lambda product: product.name)


    def store_sort(self):
        self._products.sort(key=lambda product: product.store_name)


    def price_sort(self):
        self._products.sort(key=lambda product: product.price)


    def sort_determination(self, key):
        if key == 'name':
            self._products.sort(key = lambda product: product.name)
        elif key == 'store_name':
            self._products.sort(key = lambda product: product.store_name)
        elif key == 'price':
            self._products.sort(key = lambda product: product.price)
        else:
            raise ServiceException('\n### Warning. The exception has been raised. ###\n')


    def show_products(self):
        print(f'\n~ Here is the list of products:')
        for product_id in range(len(self._products)):
            print(f"\t{product_id + 1}. {self._products[product_id].name}")
        return self._products


    def show_full_products(self):
        print(f'\n~ Here is the full list of products:')
        for product_id in range(len(self._products)):
            print(f"\t{product_id + 1}. {self._products[product_id].name} - {self._products[product_id].store_name} - {self._products[product_id].price}")
        return self._products


    def products_sum_by_ids(self, list_of_ids):
        products_list = list(map(lambda product_id: self._products[product_id - 1].name, list_of_ids))
        chosen_products = list(map(lambda product_id: self._products[product_id - 1], list_of_ids))
        price_sum = 0
        for product in chosen_products:
            price_sum = product.price + price_sum
        return products_list, round(price_sum, 3)


    @classmethod
    def generate_random_warehouse(cls, number_of_products):
        products_list = []
        list_of_possible_product_names = ["Organic Banana", "Almond Milk", "Greek Yogurt", "Whole Grain Bread",
                                          "Chicken Breast", "Extra Virgin Olive Oil", "Honey Crisp Apple", "Fresh Spinach",
                                          "Whole Wheat Pasta", "Cheddar Cheese", "Natural Peanut Butter", "Rolled Oats",
                                          "Dark Chocolate Bar", "Quinoa Grain", "Fresh Strawberries", "Canned Black Beans",
                                          "Ground Cinnamon", "Green Bell Pepper", "Maple Syrup", "Spaghetti Sauce",
                                          "Fresh Salmon Fillet", "Coconut Water", "Frozen Mixed Vegetables", "Basmati Rice",
                                          "Sweet Potatoes", "Coconut Oil", "Vegetable Broth", "Mild Salsa", "Dried Cranberries",
                                          "100% Pure Orange Juice"
]
        for product in range(number_of_products):
            product_name = list_of_possible_product_names[random.randint(0, len(list_of_possible_product_names) - 1)]
            store_name = ''.join(random.choices(string.ascii_uppercase, k=5))
            price = round(random.uniform(5.0, 100.0), 2)
            products_list. append(Product(product_name, store_name, price))

        return Warehouse(products_list)



    @staticmethod
    def show_info(found_product):
        found_product.show_info()


class BeeElephant:
    def __init__(self, bee_part: int, elephant_part: int):
        self._bee_part = bee_part
        self._elephant_part = elephant_part

    def fly(self):
        return True if self._bee_part >= self._elephant_part else False

    def trumpet(self):
        return 'tu-tu-doo-doo' if self._elephant_part >= self._bee_part else 'wzzzz'

    def eat(self, meal, value):
        meal = meal.lower()
        if meal not in ['nectar', 'grass']:
            raise ServiceException('\n### Warning: BeeElephant cannot be fed anything but nectar or grass. ###\n')
        elif meal == 'nectar':
            self._elephant_part -= value
            if self._elephant_part < 0:
                self._elephant_part = 0
            self._bee_part += value
            if self._bee_part > 100:
                self._bee_part = 100
        else:
            self._elephant_part += value
            if self._elephant_part > 100:
                self._elephant_part = 100
            self._bee_part -= value
            if self._bee_part < 0:
                self._bee_part = 0
        print('\n~ The BeeElephant has eaten and changed its size.') if value != 0 else print('\n~ Nothing to eat. The BeeElephant hasn\'t changed its size.')
        self.show_bee_elephant()


    def show_bee_elephant(self):
        print(f'\n~ Here is current BeeElephant status:',
              f'\tBee: {self._bee_part}',
              f'\tElephant: {self._elephant_part}',
              sep='\n')

class NonIterableString:
    def __init__(self, target_string: str):
        self._string = target_string


class Bus:
    def __init__(self):
        self._speed = 0
        self._max_number_of_seats = 30
        self._max_speed = 80
        self._list_of_passengers = []
        self._are_empty_seats = True
        self._is_bus_empty = True
        self._dict_of_seats = {}

    def __iadd__(self, surname):
        self._list_of_passengers.append(surname)
        return self

    def __isub__(self, surname):
        if surname in self._list_of_passengers:
            self._list_of_passengers.remove(surname)
        return self

    def _dictionary_creation(self):
        for i in range(1, 31):
            self._dict_of_seats[i] = None

    def _speedometer(self):
        if self._speed > self._max_speed:
            print('\n~ The speed of the bus is high. We need to slow down.')
            self._speed = self._max_speed
        elif self._speed <= 0:
            print('\n~ The bus has stopped.')
            self._speed = 0
        else:
            print(f'\n~ The speed has been changed. Current speed is {self._speed} kph.')

    def _are_empty_seats_determination(self):
        if len(self._list_of_passengers) == 30:
            self._are_empty_seats = False
            self._is_bus_empty = False
        elif len(self._list_of_passengers) == 0:
            self._are_empty_seats = True
            self._is_bus_empty = True
        else:
            self._are_empty_seats = True
            if len(self._list_of_passengers) >= 1:
                self._is_bus_empty = False

    def _passengers_seat_determination(self, is_passenger_in, surname):
        list_of_passengers = list(self._dict_of_seats.values())
        if is_passenger_in:
            empty_seat_id = list_of_passengers.index(None)
            self._dict_of_seats[empty_seat_id + 1] = surname
            self += surname
            self._are_empty_seats_determination()
            print(f'~ {surname} is now on the board.')
        else:
            if surname in list_of_passengers:
                passenger_seat = list_of_passengers.index(surname)
                self._dict_of_seats[passenger_seat + 1] = None
                self -= surname
                self._are_empty_seats_determination()
                print(f'~ {surname} has got off.')
            else:
                print(f'~ {surname} is not in the bus.')

    def _dict_show(self):
        print('\n~ Bus seats status:')
        for key in list(self._dict_of_seats.keys()):
            print(f'\tSeat №{key}. {self._dict_of_seats[key] if self._dict_of_seats[key] else "Empty seat."}')

    def engine_engage(self):
        print('\n~ The the engine has been engaged and the bus is ready to go.')
        self._dictionary_creation()
        self.speed_changer(speed=40)

    def engine_muffle(self):
        self.speed_changer(speed=-self._speed)
        if self._list_of_passengers:
            print()
            for passenger in self._list_of_passengers:
                self._passengers_seat_determination(False, surname=passenger)
            print('\n~ The the engine has been muffled. All the passengers need to get off.')
        else:
            print('\n~ No passengers have been left. The engine is muffled.')


    def speed_changer(self, speed):
        self._speed = self._speed + speed
        self._speedometer()

    def bus_stop(self, list_out, list_in):
        self.speed_changer(-self._speed)
        if list_out != ['']:
            print()
            for passenger in list_out:
                if not self._is_bus_empty and passenger != '':
                    self._passengers_seat_determination(False, passenger.lower().capitalize())
                elif passenger == '':
                    pass
                else:
                    print('~ The bus is already empty.')
                    break
        else:
            print('\n~ No passengers needed to leave the bus')
        if list_in != ['']:
            print()
            for passenger in list_in:
                if self._are_empty_seats and passenger != '':
                    self._passengers_seat_determination(True, surname=str(passenger.lower().capitalize()))
                elif passenger == '':
                    pass
                else:
                    print('\n~ There is no place for other passengers')
                    break
        else:
            print('\n~ No passengers have entered.')

        self.speed_changer(40)

    def bus_status(self):
        print('\n~ Here is the current bus status:')
        print(f'\tMax speed: {self._max_speed} kph',
              f'\tSpeed of the bus: {self._speed} kph',
              f'\tMax number of seats: {self._max_number_of_seats}',
              f'\tSurnames of the passengers: {self._list_of_passengers if self._list_of_passengers else "No passengers yet"}',
              sep='\n')
        self._dict_show()
