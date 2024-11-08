from functools import reduce
from time import time


def list_determination(isInt):
    while True:
        try:
            size_of_nums = int(input('\nСколько элементов будет в списке? '))
            break
        except:
            print('Размер указан некорректно')
            continue

    array = []
    while True:
        for num in range(size_of_nums):
            while True:
                try:
                    value = int(input(f'Число №{num + 1}. Введите число: ')) if isInt else str(input(f'Строка №{num + 1}. Введите строку: '))
                    array.append(value)
                    break
                except:
                    print('Ваше значение некорректно. Попробуйте еще раз')
        break

    return array


def T1_list_int_to_str():
        array = list_determination(True)
        print(f'\nВаш список чисел: {array}')
        modified_array = list(map(lambda item: str(item), array))
        print(f'Ваш список строк: {modified_array}')


def T2_nums_bigger_than_zero():
        array = list_determination(True)
        print(f'\nВаш список чисел: {array}')
        border_number = 0
        filtered_array = list(filter(lambda number: number > border_number, array))
        print(f'Cписок чисел более 0: {filtered_array}')


def T3_find_palindrome():
    array = list_determination(False)
    print(f'\nВаш список строк: {array}')
    array = map(lambda string: string.lower(), array)
    array_of_found_palindromes = list(filter(lambda string: string == string[::-1], array))
    print(f'Список строк, которые являются палиндромами: {array_of_found_palindromes}')


def flat_determination():
    while True:
        try:
            room_number = int(input('\nСколько комнат в квартире? '))
            if room_number <= 0:
                continue
            else:
                break
        except:
            print('Вы ввели некорректное значение.')

    array_of_flat = []
    while True:
        for room in range(room_number):
            dict_of_room = {
                'name': None,
                'length': None,
                'width': None
            }
            while True:
                try:
                    room_name = str(input(f'\nВведите название комнаты {room + 1}: ')).strip()
                    length = float(input('Какая у нее длина (в метрах)? '))
                    width = float(input('Какая у нее ширина (в метрах)? '))
                    if length <= 0 or width <= 0:
                        print('Такие значения для длины и ширины недопустимы.')
                        continue
                    else: pass
                except:
                    print('Создать такую комнату не получается.')
                    continue

                dict_of_room['name'] = room_name
                dict_of_room['length'] = length
                dict_of_room['width'] = width

                break
            array_of_flat.append(dict_of_room)
        break

    return array_of_flat


def time_decorator(func):
    def wrapper(*args):
        start_time = time()
        result = func(*args)
        end_time = time()
        executed_time = end_time - start_time
        return result, executed_time
    return wrapper


@time_decorator
def area_determination(array_of_flat):
    final_area = reduce(lambda prev_area, next_area: prev_area + next_area, map(lambda dictionary: dictionary['length'] * dictionary['width'], array_of_flat))

    return final_area


def T4_T5_flat_area():
    array_of_flat = flat_determination()
    flat_show(array_of_flat)
    final_area, executed_time = area_determination(array_of_flat)
    print(f'\nПлощадь квартиры составляет: {final_area} м².')
    print(f'Время работы программы составило: {executed_time} секунд.')


def flat_show(array_of_flats):
    list_of_strings = list(map(lambda dict: f'{dict["name"]}: {dict["length"]}м на {dict["width"]}м.', array_of_flats))

    print('\nВаши комнаты:')
    for string in list_of_strings:
        print(string)



def menu():
    menu_points = '\n1. Список чисел в список строк;\n' \
                  '2. Вывести числа больше 0;\n' \
                  '3. Найти все палиндромы;\n' \
                  '4. Посчитать площадь квартиры;\n' \
                  '5. Завершить.'
    while True:
        while True:
            try:
                choice = int(input(f'{menu_points}\n\nВыберите пункт: '))
                if choice <= 0 or choice > 5:
                    print('Вы выбрали несуществующий пункт.')
                    continue
                else: break
            except:
                print('Вы ввели неправильное значение.')
                continue

        match choice:
            case 1:
                T1_list_int_to_str()
            case 2:
                T2_nums_bigger_than_zero()
            case 3:
                T3_find_palindrome()
            case 4:
                T4_T5_flat_area()
            case 5:
                return False


if __name__ == '__main__':
    menu()

