from math import pi

class Soda:
    def __init__(self, taste = None):

        self._taste = taste

    def soda_taste(self):
        if self._taste:
            if self._taste[0].lower() in ['a', 'e', 'u', 'i', 'o']:
                article = 'an'
            else:
                article = 'a'
            print(f"\n~ You've got {article} {self._taste.lower()}-flavored soda.")
        else:
            print("\n~ You've got a regular soda.")


class Math:
    def __init__(self):
        pass

    def addition(self, num_1, num_2):
        result = num_1 + num_2
        self.show_result(num_1=num_1, num_2=num_2, result=result, operation='+')
        return result

    def subtraction(self, num_1, num_2):
        result = num_1 - num_2
        self.show_result(num_1=num_1, num_2=num_2, result=result, operation='-')
        return result

    def multiplication(self, num_1, num_2):
        result = num_1 * num_2
        self.show_result(num_1=num_1, num_2=num_2, result=result, operation='*')
        return result

    def division(self, num_1, num_2):
        result = num_1 / num_2
        self.show_result(num_1=num_1, num_2=num_2, result=result, operation='/')
        return result

    def show_result(self, num_1, num_2, result, operation):
        print(f'\n~ {num_1} {operation} {num_2} = {result:.2f}')


class Car:
    def __init__(self, car_type, year, color):
        self._car_type = car_type
        self._year = year
        self._color = color
        self._is_engine_on = False

    def engage(self):
        if not self._is_engine_on:
            print('\n~ The engine has been engaged successfully.')
            self._is_engine_on = True
        else:
            print('\n~ The engine is already engaged.')

    def muffle(self):
        if not self._is_engine_on:
            print('\n~ The engine is not engaged. No need to muffle it.')
        else:
            print('\n~ The engine has been muffled successfully.')
            self._is_engine_on = False

    def set_color(self, color):
        if color.lower() == self._color.lower():
            print('\n~ The new color is the same.')
        else:
            self._color = color
            print(f'\n~ The color has been successfully changed to {self._color}.')


    def set_year(self, year):
        if year == self._year:
            print('\n~ The year of the release is the same.')
        else:
            self._year = year
            print(f'\n~ The year of the car has been successfully changed to {self._year}.')

    def set_car_type(self, car_type):
        if car_type.lower() == self._car_type.lower():
            print('\n~ The type of the car is the same.')
        else:
            self._car_type = car_type
            print(f'\n~ The type of the car has been successfully changed to {self._car_type}.')


    def get_info(self):
        print(f'\n~ Your car type is {self._car_type}. The car is {self._color}. The year of release is {self._year}.'
              f' Current engine state: {"Engaged" if self._is_engine_on else "Muffled"}.')


class Sphere:
    def __init__(self, radius=1, x_coord=0, y_coord=0, z_coord=0):
        self._radius = radius
        self._x_coord = x_coord
        self._y_coord = y_coord
        self._z_coord = z_coord

    def ball_volume(self):
        volume = round(4 * pi * self._radius ** 3 / 3, 3)
        return volume

    def get_square(self):
        esa = round(4 * pi * self._radius ** 2, 3)
        return esa

    def get_radius(self):
        return self._radius

    def get_center(self):
        coord_tuple = (self._x_coord, self._y_coord, self._z_coord)
        return coord_tuple

    def set_radius(self, radius):
        self._radius = radius
        print(f'\n~ The radius of the sphere is {self._radius} cm.')

    def set_center(self, x_coord, y_coord, z_coord):
        self._x_coord = x_coord
        self._y_coord = y_coord
        self._z_coord = z_coord
        print(f'\n~ The coords have been changed:',
              f'  x_coord: {self._x_coord}',
              f'  y_coord: {self._y_coord}',
              f'  z_coord: {self._z_coord}',
              sep='\n'
        )

    def is_point_inside(self, x_coord, y_coord, z_coord):
        equation = (x_coord - self._x_coord)**2 + (y_coord - self._y_coord)**2 + (z_coord - self._z_coord)**2 <= self._radius ** 2
        if equation:
            print(f'\n~ The point {(x_coord, y_coord, z_coord)} is inside the sphere.')
            return True
        else:
            print(f'\n~ The point {(x_coord, y_coord, z_coord)} is outside the sphere.')
            return False

    def show_info(self):
        print(f'\n~ The coords of the sphere: ',
              f'  x_coord: {self._x_coord};',
              f'  y_coord: {self._y_coord};',
              f'  z_coord: {self._z_coord}.',
              f'  The radius of the sphere is {self._radius} cm.',
              sep='\n')


class SuperStr(str):
    def __init__(self, super_str):
        self._super_str = super_str

    def is_repetition(self, string):
        if not string or not self._super_str:
            return False

        if len(self._super_str) % len(string) != 0:
            return False

        max_reps = len(self._super_str) // len(string)
        obtained_string = string * max_reps

        if self._super_str == obtained_string:
            return True
        else:
            return False

    def is_palindrome(self):
        if self._super_str.lower() == self._super_str[::-1].lower():
            return True
        else:
            return False