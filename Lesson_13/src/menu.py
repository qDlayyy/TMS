from src.classes import (PizzaDirector, AnimalFactory, Calculator, Addition,
                         Subtraction, Multiplication, Division, Fibonacci, EndlessSeries)
from src.service import InputCheck, ServiceException


class T1FibonacciSeries:
    def __init__(self):
        pass

    @staticmethod
    def limit_determination():
        while True:
            try:
                number = input('\n How many numbers should be in Fibonacci series: ')
                number = InputCheck.inc(target_number=number)
                number = InputCheck.greater(target_number=number, border_number=0)
                return number
            except Exception as e:
                print(e)


    def execute(self):
        fibonacci_limit = self.limit_determination()
        fibonacci = Fibonacci(limit=fibonacci_limit)

        fibonacci.fibonacci_create()


class T2EndlessSeries:
    def __init__(self):
        pass

    @staticmethod
    def _limit_determination():
        while True:
            try:
                number = input('\n How many numbers the endless series should consist of: ')
                number = InputCheck.inc(target_number=number)
                number = InputCheck.greater(target_number=number, border_number=0)
                return number
            except Exception as e:
                print(e)

    @staticmethod
    def list_of_numbers_determination():
        while True:
            try:
                string = input('\nEnter all the numbers using SPACE as separator: ').strip()
                string = InputCheck.string_separator_check(permissible_separators=[' '], target_string=string)
                return string.split(' ')
            except Exception as e:
                print(e)

    def execute(self):
        limit = self._limit_determination()
        list_of_numbers = self.list_of_numbers_determination()
        series = EndlessSeries(limit=limit, list_of_numbers=list_of_numbers)

        series.endless_series_show()


class T3PizzaBuilder:
    def __init__(self):
        self._dict_of_ingredients = {
            'size': None,
            'cheese': None,
            'pepperoni': None,
            'mushroom': None,
            'onions': None,
            'bacon': None
        }

    @staticmethod
    def _answer_determination(target_string):
        if target_string in ['yes', 'y']:
            return True
        elif target_string in ['no', 'n']:
            return False
        else:
            return None


    def execute(self):
        pizza_director = PizzaDirector()
        for ingredient in self._dict_of_ingredients:
            while True:
                try:
                    if ingredient == 'size':
                        string = input('\nWhat is the size of the pizza (cm)? ')
                        string = InputCheck.inc(target_number=string)
                    else:
                        string = input(f'\nDo you want to add {ingredient}? Answer yes(y) or no(n): ').strip().lower()
                        error_message = '\n### Warning. The answer must be yes(y) or no(n) only. Try again. ###\n'
                        string = InputCheck.valid_string(target_string=string, list_of_string_variants=['y', 'yes', 'no', 'n'], error_message=error_message)
                        string = self._answer_determination(target_string=string)
                    if string is not None:
                        self._dict_of_ingredients[ingredient] = string

                    break

                except Exception as e:
                    print(e)

        pizza = pizza_director.make_pizza(size=self._dict_of_ingredients['size'],
                                  cheese=self._dict_of_ingredients['cheese'],
                                  pepperoni=self._dict_of_ingredients['pepperoni'],
                                  mushrooms=self._dict_of_ingredients['mushroom'],
                                  onions=self._dict_of_ingredients['onions'],
                                  bacon=self._dict_of_ingredients['bacon'])
        pizza_director.show_pizza(pizza=pizza)


class T4AnimalFactory:
    def __init__(self):
        pass

    @staticmethod
    def execute():
        factory = AnimalFactory()
        while True:
            try:
                string = input('\nWhat animal are you going to create: ').strip().lower()
                string = InputCheck.valid_string(target_string=string, list_of_string_variants=['cat', 'dog'])
                break
            except Exception as e:
                print(e)

        animal = factory.create_animal(animal_choice=string)
        animal.speak()


class T5CalculatorStrategy:
    def __init__(self):
        pass

    @staticmethod
    def _params_determination():
        while True:
            try:
                string_num_1 = input('\nWhat is the first number? ').strip()
                numb_1 = InputCheck.fnc(target_number=string_num_1)

                operation = input('What is the operation (+, -, *, /)? ').strip()
                operation = InputCheck.sign_search(target_string=operation,
                                                   list_of_sign_variants=['+', '-', '*', '/'])
                if operation is None:
                    raise ServiceException('\n### Warning. Invalid operation. ###')

                string_num_2 = input('What is the second number? ').strip()
                num_2 = InputCheck.fnc(target_number=string_num_2)

                if operation == '/' and num_2 == 0:
                    raise ServiceException('\n### Warning. Divider cannot be 0. ###\n')

                return numb_1, num_2, operation

            except Exception as e:
                print(e)

    def execute(self):
        num_1, num_2, operation = self._params_determination()
        calculator = Calculator()
        result = None

        match operation:
            case '+':
                calculator.set_strategy(strategy=Addition())
                result = calculator.calculate(num_1=num_1, num_2=num_2)
            case '-':
                calculator.set_strategy(strategy=Subtraction())
                result = calculator.calculate(num_1=num_1, num_2=num_2)
            case '*':
                calculator.set_strategy(strategy=Multiplication())
                result = calculator.calculate(num_1=num_1, num_2=num_2)
            case '/':
                calculator.set_strategy(strategy=Division())
                result = calculator.calculate(num_1=num_1, num_2=num_2)
            case None:
                print('\n### Warning. Something went wrong. ###\n')
                return

        if result or result == 0:
            print(f'\n~ {num_1} {operation} {num_2} = {result:.2f}')


class Exit:
    def __init__(self):
        pass

    @staticmethod
    def execute():
        exit()


class Menu:
    def __init__(self):
        self._items = [
            {'point': '\n1. Fibonacci series', 'action': T1FibonacciSeries()},
            {'point': '2. Endless series', 'action': T2EndlessSeries()},
            {'point': '3. Pizza Builder', 'action': T3PizzaBuilder()},
            {'point': '4. Animal Factory', 'action': T4AnimalFactory()},
            {'point': '5. Calculator Strategy', 'action': T5CalculatorStrategy()},
            {'point': '6. Exit', 'action': Exit()}
        ]

    def _menu_point_determination(self):
        while True:
            try:
                choice = input('\nWhat Menu point you choose: ').strip()
                choice = InputCheck.within(target_number=choice, target_list=self._items)
                return choice
            except Exception as e:
                print(e)

    def _menu_show(self):
        list(map(lambda item: print(item['point']), self._items))

    def run(self):
        while True:
            try:
                self._menu_show()
                choice = self._menu_point_determination()

                self._items[choice - 1]['action'].execute()
            except Exception as e:
                print(e)
