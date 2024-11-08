from abc import abstractmethod


## Fibonacci Series
class Fibonacci:
    def __init__(self, limit):
        self._limit = limit
        self._array_of_numbers = list(self._fibonacci())

    def _fibonacci(self):
        prev_num, next_num = 0, 1

        for _ in range(self._limit):
            yield prev_num
            prev_num, next_num = next_num, prev_num + next_num

    def _fibonacci_iter_row_creation(self):
        generator_fibonacci = Fibonacci._fibonacci(self._limit)
        self._array_of_numbers = list(map(lambda num: num, generator_fibonacci))

    def fibonacci_create(self):
        print(f'\n~ Fibonacci series for the first {len(self._array_of_numbers)} fibonacci numbers: '
              f'{", ".join(map(lambda num: str(num), self._array_of_numbers))}.')


## Endless Series
class EndlessSeries:
    def __init__(self, limit, list_of_numbers):
        self._limit = limit
        self._list_of_numbers = list_of_numbers
        self._line = ''

    def _endless_series_generator(self):
        while True:
            for num in self._list_of_numbers:
                yield num

    def _endless_series_line_creation(self):
        generator = self._endless_series_generator()
        for _ in range(self._limit):
            self._line += next(generator) + '-'

        self._line = self._line[:-1]

    def endless_series_show(self):
        self._endless_series_line_creation()
        print(f'\n~ Endless number series in range of {self._limit}: {self._line}.')


## Pizza Builder
class Pizza:
    def __init__(self):
        self.size = None
        self.cheese = None
        self.pepperoni = None
        self.mushrooms = None
        self.onions = None
        self.bacon = None

    def __str__(self):
        return (f"\n~ Your Pizza:\n"
                f"\tSize: {self.size} cm.\n"
                f"\tCheese: {'Added' if self.cheese else 'Absent'}\n"
                f"\tPepperoni: {'Added' if self.pepperoni else 'Absent'}\n"
                f"\tMushrooms: {'Added' if self.mushrooms else 'Absent'}\n"
                f"\tOnions: {'Added' if self.onions else 'Absent'}\n"
                f"\tBacon: {'Added' if self.bacon else 'Absent'}.")

class PizzaBuilder:
    def __init__(self):
        self._pizza = Pizza()

    def set_size(self, size: int):
        self._pizza.size = size
        return self

    def set_cheese(self, cheese: bool):
        self._pizza.cheese = cheese
        return self

    def set_pepperoni(self, pepperoni: bool):
        self._pizza.pepperoni = pepperoni
        return self

    def set_mushrooms(self, mushrooms: bool):
        self._pizza.mushrooms = mushrooms
        return self

    def set_onions(self, onions: bool):
        self._pizza.onions = onions
        return self

    def set_bacon(self, bacon: bool):
        self._pizza.bacon = bacon
        return self

    def build(self):
        return self._pizza

class PizzaDirector:
    def __init__(self):
        self._pizza_builder = PizzaBuilder()

    def make_pizza(self, size, cheese, pepperoni, mushrooms, onions, bacon):
        pizza = (
            self._pizza_builder
            .set_size(size=size)
            .set_cheese(cheese=cheese)
            .set_pepperoni(pepperoni=pepperoni)
            .set_mushrooms(mushrooms=mushrooms)
            .set_onions(onions=onions)
            .set_bacon(bacon=bacon)
            .build()
        )
        return pizza

    def show_pizza(self, pizza):
        print(pizza)


## Animal Fabric Method
class Animal:
    def __init__(self):
        pass
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def __init__(self):
        super().__init__()

    def speak(self):
        print('\n~ woof-woof-woof')

class Cat(Animal):
    def __init__(self):
        super().__init__()

    def speak(self):
        print('\n~ meow-meow-meow')

class AnimalFactory:

    def __init__(self):
        pass

    @staticmethod
    def create_animal(animal_choice):
        if animal_choice == 'dog':
            return Dog()
        elif animal_choice == 'cat':
            return Cat()
        else:
            print('How have you managed to even get here?')


## Calculator Strategy
class AbstractOperation:
    @abstractmethod
    def execute(self, num_1, num_2):
        pass

class Calculator:
    def __init__(self):
        self._strategy = None

    def set_strategy(self, strategy: AbstractOperation):
        self._strategy = strategy

    def calculate(self, num_1, num_2):
        return self._strategy.execute(num_1, num_2)

class Addition(AbstractOperation):

    def execute(self, num_1, num_2):
        return num_1 + num_2

class Subtraction(AbstractOperation):

    def execute(self, num_1, num_2):
        return num_1 - num_2

class Multiplication(AbstractOperation):

    def execute(self, num_1, num_2):
        return num_1 * num_2

class Division(AbstractOperation):

    def execute(self, num_1, num_2):
        return num_1 / num_2


