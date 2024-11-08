from typing import Union

class ServiceException(Exception):
    def __init__(self, message: str = ''):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message if self.message else ''

class InputCheck:
    def __init__(self):
        pass

    @classmethod
    def within(cls, target_number: Union[int, str, float], target_list):
        """
        Checks if target_number is in the limit of target_list elements amount and cannot be negative or 0.
        Otherwise, raises ServiceException.

        :param target_number: Checked number
        :type target_number: Union[int, str, float]
        :param target_list: List of any items
        :return: int
        """
        try:
            target_number = int(target_number)
            if target_number < 1 or target_number > len(target_list):
                raise ServiceException('\n### Warning. Incorrect menu point. Try again. ###\n')
            return target_number
        except ValueError:
            raise ServiceException('\n### Warning. Not a number was entered. Try again. ###\n')

    @classmethod
    def inc(cls, target_number: Union[int, str, float]):
        """
        Checks if target_number is an integer. Otherwise, raises ServiceException.
        :param target_number: Checked number
        :type target_number: Union[int, str, float]
        :return: int
        """
        try:
            target_number = int(target_number)
            return target_number
        except:
            raise ServiceException('\n### Warning. Not an integer number was entered. Try again. ###\n')

    @classmethod
    def fnc(cls, target_number: Union[int, float, str]):
        """
                Checks if target_number is a float number. Otherwise, raises ServiceException.
                :param target_number: Checked number
                :type target_number: Union[int, str, float]
                :return: float
                """
        try:
            number = float(target_number)
            return number
        except:
            raise ServiceException('\n### Warning. Not a number. Try again. ###\n')

    @classmethod
    def between(cls, target_number: Union[int, float], border_nums_tuple: tuple[Union[int, float], Union[int, float]]):
        """
        Checks if target_number is in range of two integer or float number from border_nums_tuple.
        Otherwise, raises ServiceException.

        :param target_number: Checked number
        :type target_number: Union[int, float]
        :param border_nums_tuple: Tuple with two numbers either integers or floats
        :type border_nums_tuple: tuple[Union[int, float], Union[int, float]]
        :return: Union[int, float]
        """
        if not border_nums_tuple[0] <= target_number:
            raise ServiceException('\n### Warning. This number is too small for that case. Try again. ###\n')
        elif not target_number <= border_nums_tuple[1]:
            raise ServiceException('\n### Warning. This number is too big for that case. Try again. ###\n')
        else:
            return target_number

    @classmethod
    def nes(cls, target_string: str):
        """
        Checks if the string is not empty. Otherwise, raises ServiceException.
        :param target_string: Checked string
        :type target_string: str
        :return: str
        """
        if target_string:
            return target_string
        else:
            raise ServiceException('\n### Warning. The string is empty. Try again. ###\n')

    @classmethod
    def greater(cls, target_number: Union[int, float], border_number: Union[int, float]):
        """
        Checks if target_number is greater than border_number and returns target number.
        Otherwise, raises ServiceException.

        :param target_number: Checked number
        :type target_number: Union[int, float]
        :param border_number: The number being compared to
        :type border_number: Union[int, float]
        :return: Union[int, float]
        """
        if target_number > border_number:
            return target_number
        else:
            raise ServiceException('\n### Warning. The number is too small. Try again. ###\n')

    @classmethod
    def nums_within(cls, list_of_numbers: list[int], target_list: list):
        """
        Creates a list with all the integer numbers that are greater than 0 and smaller than the amount of items in the list.
        Otherwise, raises ServiceException.

        :param list_of_numbers: List of numbers to check
        :type list_of_numbers: list[int]
        :param target_list: List with items to range
        :type target_list: list

        :return: list[int]
        """
        try:
            print(len(target_list))
            new_list_of_nums = list(filter(lambda current_number: 0 < current_number <= len(target_list), list_of_numbers))
            return new_list_of_nums
        except ValueError:
            raise ServiceException('\n### Warning. Not a number was entered. Try again. ###\n')
        except:
            raise ServiceException('\n### Warning. Something went wrong with the choice. Try again. ###\n')

    @classmethod
    def multiple_int_inputs_range_check(cls, list_of_input_nums: list[Union[int, float, str]], range_tuple: tuple[Union[int, float], Union[int, float]]):
        """
        Checks every item of list_of_input_nums. It should be integer, and equal or greater than range_tuple[0] and
        equal or smaller than range_tuple[1]. Returns list of all suitable numbers.
        Otherwise, raises ServiceException.

        :param list_of_input_nums: list of items to check
        :type list_of_input_nums: list[Union[int, float, str]]
        :param range_tuple: tuple with two numbers border numbers
        :type range_tuple: tuple[Union[int, float], Union[int, float]]
        :return: list[Union[int, float]]
        """
        array_of_inputs = []
        for text in list_of_input_nums:
            while True:
                try:
                    target_value = input(text)
                    target_value = cls.inc(target_number=target_value)
                    target_value = cls.between(target_number=target_value, border_nums_tuple=range_tuple)
                    array_of_inputs.append(target_value)
                    break
                except Exception as e:
                    print(e)
        return array_of_inputs

    @classmethod
    def string_separator_check(cls, permissible_separators: list, target_string: str):
        """
        Checks all possible separator variants in target_string.
        If there is no forbidden separators returns target_string. Otherwise, raises ServiceException.

        :param permissible_separators: All acceptable separators
        :type permissible_separators: list
        :param target_string: Checked string
        :type target_string: str
        :return: str
        """
        possible_separators = [',', '.', '|', '&', ' ']
        forbidden_separators = list(filter(lambda separator: separator not in permissible_separators, possible_separators))
        for separator in forbidden_separators:
            if separator in target_string:
                permissible_separators[permissible_separators.index(' ')] = "SPACE"
                raise ServiceException(f'\n### Warning. The string must have only {permissible_separators} separators. '
                                       f'Got "{separator}" instead. ###\n')

        return target_string

    @classmethod
    def valid_string(cls, target_string: str, list_of_string_variants: list, error_message = None):
        """
        Checks if the string valid by going through all the options on the list_of_string_variants. Returns target_string.
        Otherwise, raises ServiceException.

        :param target_string: Checked string
        :type target_string: str
        :param list_of_string_variants: List of valid variants
        :type list_of_string_variants: list
        :param error_message: Optional error message
        :type error_message: _SpecialForm[str, None]
        :return: str
        """
        if target_string not in list_of_string_variants:
            if error_message:
                raise ServiceException(message=error_message)
            else:
                raise ServiceException('\n### Warning. Invalid variant. Try again ###\n')
        else:
            return target_string

    @classmethod
    def sign_search(cls, target_string: str, list_of_sign_variants: list):
        """
        Searching for every sign of list_of_sign_variants in target_string. Returns the first met sign.
        Otherwise, returns None

        :param target_string: The string where the function tries to find any sign of list_of_sign_variants
        :type target_string: str
        :param list_of_sign_variants: list of sign variants
        :type list_of_sign_variants: list
        :return: str or None
        """
        for sign in list_of_sign_variants:
            if sign in target_string:
                return str(sign)
        return None





