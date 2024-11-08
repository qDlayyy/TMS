import re

class InputException(Exception):
    pass


class InputCheck:
    def __init__(self):
        pass

    def menu_point_validation(self, choice, menu_length):
        try:
            choice = int(choice)
            if choice <= 0 or choice > menu_length:
                raise InputException('\n### Warning. Incorrect menu point. Try again.')
        except ValueError:
            raise InputException('\n### Warning. Not a number has been entered. Try again.')
        return choice

    def word_determination(self, string):
        word_pattern = r'[a-zA-Z]+'
        if string:
            if not re.match(word_pattern, string):
                raise InputException('\n### Warning. The word cannot consist of anything but letters. Try again.\n')
            else:
                pass
        else:
            string = None
        return string

    def math_number_check(self, number_1, number_2):
        try:
            number_1 = float(number_1)
            number_2 = float(number_2)
        except:
            raise InputException('\n### Warning. This is not a pair of numbers. Try again.\n')
        return number_1, number_2

    def math_number_division_check(self, number_1, number_2):
        try:
            number_1 = float(number_1)
            number_2 = float(number_2)
            if number_2 == 0:
                raise InputException('\n### Warning. Delimiter cannot be 0. Try again.\n')
            else:
                pass
        except ValueError:
            raise InputException('\n### Warning. This is not a pair of numbers. Try again.\n')
        return number_1, number_2

    def input_check_branching(self, input_text, method):
        while True:
            try:
                input_string = input(input_text)
                string = method(input_string)
                break
            except Exception as exception:
                print(exception)
        return string

    def four_digit_number_determination(self, number):
        four_digit_pattern = r'[0-9]{4}'
        if number:
            if not re.match(four_digit_pattern, number):
                raise InputException('\n### Warning. This number is incorrect. Try again.\n')
            else:
                return number
        else:
            raise InputException('\n### Warning. The year of the car cannot be empty. Try again.\n')

    def sphere_radius_check(self, radius):
        try:
            if radius:
                radius = float(radius)
                if radius <= 0:
                    raise InputException('\n ### Warning. The sphere radius cannot be negative. Try again.\n')
                else:
                    return radius
            else:
                return None
        except ValueError:
            raise InputException('\n### Warning. The sphere radius cannot be something, but a number. Try again.\n')

    def sphere_coord_check(self, coord):
        try:
            if coord:
                coord = float(coord)
                return coord
            else:
                return None

        except ValueError:
            raise InputException('\n### Warning. The coord cannot be something, but a number. Try again.\n')

    def yes_or_no_determination(self, string):
        if string.lower() in ['y', 'yes']:
            return True
        elif string.lower() in ['n', 'no']:
            return False
        elif string.lower() in ['r', 'radius']:
            return None
        else:
            raise InputException(
                '\n### Warning. Cannot clearly understand your answer, use "y"/"yes", "n"/"no" or "r"/"radius". Try again.')
