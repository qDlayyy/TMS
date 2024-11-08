from typing import Union

class ServiceException(Exception):
    pass

class InputCheck:
    def __init__(self):
        pass

    @classmethod
    ## Menu Input Check
    def mic(cls, choice, menu_list):
        try:
            choice = int(choice)
            if choice < 1 or choice > len(menu_list):
                raise ServiceException('\n### Warning. Incorrect menu point. Try again. ###\n')
            return choice
        except ValueError:
            raise ServiceException('\n### Warning. Not a number was entered. Try again. ###\n')


    @classmethod
    ## Integer number check
    def inc(cls, target_number):
        try:
            target_number = int(target_number)
            return target_number
        except:
            raise ServiceException('\n### Warning. Not an integer number was entered. Try again. ###\n')


    @classmethod
    ## Number Between Two Check
    def nbtc(cls, target_number: Union[int, float], border_nums_tuple: tuple):
        if not border_nums_tuple[0] <= target_number:
            raise ServiceException('\n### Warning. This number is too small for that case. Try again. ###\n')
        elif not target_number <= border_nums_tuple[1]:
            raise ServiceException('\n### Warning. This number is too big for that case. Try again. ###\n')
        else:
            return target_number

    @classmethod
    ## Not empty string
    def nes(cls, string):
        if string:
            return string
        else:
            raise ServiceException('\n### Warning. The string is empty. Try again. ###\n')


    @classmethod
    def list_of_nums_within_the_list(cls, list_of_numbers, menu_list):
        try:
            print(len(menu_list))
            new_list_of_nums = list(filter(lambda current_number: 0 < current_number <= len(menu_list), list_of_numbers))
            return new_list_of_nums
        except ValueError:
            raise ServiceException('\n### Warning. Not a number was entered. Try again. ###\n')
        except:
            raise ServiceException('\n### Warning. Something went wrong with the choice. Try again. ###\n')

    @classmethod
    def multiple_int_inputs_range_check(cls, list_of_input_texts: list, range_tuple: tuple):
        array_of_inputs = []
        for text in list_of_input_texts:
            while True:
                try:
                    target_value = input(text)
                    target_value = cls.inc(target_number=target_value)
                    target_value = cls.nbtc(target_number=target_value, border_nums_tuple=range_tuple)
                    array_of_inputs.append(target_value)
                    break
                except Exception as e:
                    print(e)
        return array_of_inputs

    @classmethod
    def string_separator_check(cls, permissible_separators: list, target_string: str):
        possible_separators = [',', '.', '|', '&', ' ']
        forbidden_separators = list(filter(lambda separator: separator not in permissible_separators, possible_separators))
        for separator in forbidden_separators:
            if separator in target_string:
                permissible_separators[permissible_separators.index(' ')] = "SPACE"
                raise ServiceException(f'\n### Warning. The string must have only {permissible_separators} separators. '
                                       f'Got "{separator}" instead. ###\n')

        return target_string





