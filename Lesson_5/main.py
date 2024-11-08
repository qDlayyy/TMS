import math
import random
from math import factorial

def value_input (promt, validation_is_a_number):
    while True:
        value = (input(promt))
        if validation_is_a_number(value):
            value = int(value)
            return value
        else: print('Значение введено некоректно.')

def validation_is_a_number (value):
    return value.isdigit() and int(value) >= 0

def sin_cos(isSin):
    """
    Для ряда тейлора использовать градусы нельзя. Данные формулы предназначены для вычисления синуса и косинуса,
    используя радианы. Так как пользователю удобнее использовать градусы, мы используем math для преобразования градусов
    в радианы.
    """

    promt_x = 'Введите велечину некоторого угла в градусах: '
    promt_n = 'Введите значение n (чем значение больше, тем точнее результат): '
    x = value_input(promt_x, validation_is_a_number)
    limit = value_input(promt_n, validation_is_a_number)
    sum = 0
    radian_x = math.radians(x)
    if isSin:
        print('\n===Sin===\n')
        for n in range(limit):
            sum += (-1) ** n * (radian_x ** (2 * n + 1)) / factorial(2 * n + 1)
        print(f'При n = {n} Sin(x) = {sum:.6f}.')
    else:
        print('\n===Cos===\n')
        sum = 0
        for n in range(limit):
            sum += ((-1) ** n) * (radian_x ** (2 * n)) / factorial(2 * n)
        print(f'При n = {n}, Cos(x) = {sum:.6f}.')


def money_saver ():
    """
    Мы можем сильно ускорить работу программы, добавив проверку на возможность выполнения условия. Если сумма, отложенная
    за 6 дней не будет превышать еженедельные затраты на поход в кино, то накопить на телефон Маше невозможно.
    """
    phone_prompt = 'Сколько стоит телефон (руб.): '
    save_amount_prompt ='Сколько рублей Маша может откладывать каждый день: '
    cinema_cost_prompt = 'Во сколько рублей обходится еженедельный поход в кино для Маши: '
    phone_price = value_input(phone_prompt, validation_is_a_number)
    saved_money = value_input(save_amount_prompt, validation_is_a_number)
    cinema_cost = value_input(cinema_cost_prompt, validation_is_a_number)

    if saved_money * 6 <= cinema_cost:
        print('\nС таким условием Маша никогда не накопит на телефон')
    else:
        current_money_in_pocket = 0
        day_count = 1 #Понедельник - 1, вторник - 2 и т.д.
        while current_money_in_pocket < phone_price:
            if day_count % 7 :
                current_money_in_pocket += saved_money
                day_count += 1
            else:
                current_money_in_pocket -= cinema_cost
                day_count += 1
        day_count -= 1
        print(f'\nМаша накопит на телефон стоимостью {phone_price} рублей за {day_count} дней.',
              f'При этом Маша должна 6 дней в неделю откладывать {saved_money} рублей и тратить на воскресное кино не более {cinema_cost} рублей.',
              sep='\n')


def fibonacci_series ():
    amount_promt = 'Ряд из скольки чисел требуется вывести: '
    amount = value_input(amount_promt, validation_is_a_number)

    prev_digit = 0
    current_digit = 1
    line = ''
    for attempt in range(amount - 1):
        if line == '':
            line += str(prev_digit) + ' '
        line += str(current_digit) + ' '
        current_digit, prev_digit = current_digit + prev_digit, current_digit
    line = f'({line.strip()})'
    print(f'Первые {amount} числа ряда Фибоначчи: {line}')


def str_to_list (string):
    string.strip()
    array = string.split(' ')
    array = list(map(int, array))
    return array


def sum_min_max():
    string = input('Введите список целых значений через пробел: ')
    array = str_to_list(string)
    max_num = max(array)
    min_num = min(array)
    sum_of_array = sum(array)

    print(f'\nСписок чисел пользователя: {array}',
          f'Сумма всех чисел списка: {sum_of_array}',
          f'Максимальное значение: {max_num}',
          f'Минимальное значение: {min_num}',
          sep='\n')


def find_reps ():
    """
    Создаем список из строки. Сохраняем количество каждого встречающегося элемента в словарь, где ключом является число,
    а значением - количество повторений. Получив все ключи словаря в виде списка, мы можем узнать какие ключи (числа)
    повторяются более одного раза.
    """
    string = input('Введите список целых значений через пробел: ')
    array = str_to_list(string)
    dict_of_entries = {}
    result_dict ={}


    for number in array:
        dict_of_entries[number] = dict_of_entries.get(number, 0) + 1

    keys = list(dict_of_entries.keys())
    for key in keys:
        if dict_of_entries[key] > 1:
            result_dict[key] = dict_of_entries[key]

    print('\nВ списке нет повторяющихся значений.' if not result_dict else f'\nВ списке есть повторения: {result_dict}')


def binary_search():
    """
    Проверяем массив на уникальность с помощью преобразования в множество, сортируем его по возрастанию. Далее обозначаем
    нижниюю и верхнюю границу поиска. Находим средний элемент в обозначенном границами промежутке. Если число, на которое
    мы попали не равно искомому, то проверяем больше оно или меньше. В зависимости от этого двигаем правую или левую границу
    соответственно. Проделываем этот алгоритм до тех пор пока не попадем в нужное число."""
    unique_array = list_creations()
    flag = False
    while not flag:
        try:
            searching_number = int(input('Введите число, позицию которого требуется найти: '))
            flag = True
        except:
            print("Вы ввели не число.")

    found_number_index = binary_search_algorithm(unique_array, searching_number)

    if found_number_index is None:
        print(f'\nЗначения {searching_number} нет в списке {unique_array}.')
    else:
        print(f'\nЗначение {searching_number} находится в спике {unique_array} под индексом {found_number_index}.')


def list_creations ():
    acceptance_flag = False
    while not acceptance_flag:
        print(
            '1. Создать список вручную;',
            '2. Сгенерировать список.',
            sep='\n'
        )
        choice = int(input('Выберете пункт: '))
        if 2 > choice < 1: continue
        match choice:
            case 1:
                string = input('\nВведите список целых и уникальных значений через пробел: ')
                array = str_to_list(string)
                unique_array = []
                if len(set(array)) != len(array):
                    unique_set = set(array)
                    needed_length = len(array)
                    while len(unique_set) != needed_length:
                        unique_set.add(random.randint(0, 100))
                    unique_array = sorted(list(unique_set))
                    print(f'\nВ вашем списке были найдены повторяющеся значения. Список был изменен: {unique_array}')
                else:
                    unique_array = sorted(array)
                    print(f'\nВаш упорядоченный список значений: {unique_array}')
                acceptance_flag = True
            case 2:
                length_of_set = 20
                unique_set = set()
                while len(unique_set) < length_of_set:
                    unique_set.add(random.randint(0, 100))
                unique_array = sorted(list(unique_set))
                print(f'\nВот сгенерированный список из {length_of_set} значений: {unique_array}.')
                acceptance_flag = True

    return unique_array


def binary_search_algorithm (unique_array, number):
    left_index = 0
    right_index = len(unique_array) - 1
    found_number_index = None

    while left_index <= right_index:
        current_index = (left_index + right_index) // 2
        if unique_array[current_index] == number:
            found_number_index = current_index
            return found_number_index
        elif unique_array[current_index] < number:
            left_index = current_index + 1
        else:
            right_index = current_index - 1

    return found_number_index


def binary_search_with_bias ():

    """
    Предусматривается, что строка, введенная пользователем отсортирована и может иметь некоторое смещение. Если строка
    будет введена неправильно или будут встречаться повторяющиеся значения, то код может работать некорректно. Принцип бинарного
    поиска тот же. Единственное, что мы запоминаем наш сдвиг (находим наименьшее значение и смотрим его id) и позже, когда применили
    бинарный поиск к отсортированному списку, учитываем ранее найденный сдвиг.
    """

    string = input('Введите список целых и уникальных значений через пробел. Вы можете сместить значения влево или вправо: ')
    array = str_to_list(string)
    min_in_array = min(array)
    bias = array.index(min_in_array)
    sorted_array = sorted(array)
    flag = False
    while not flag:
        try:
            searching_number = int(input('Введите число, позицию которого требуется найти: '))
            flag = True
        except:
            print("Вы ввели не число.")

    found_number_index = binary_search_algorithm(sorted_array, searching_number)
    if found_number_index is None:
        print(f'\nЗначения {searching_number} нет в списке {array}.')
    elif found_number_index + bias > len(sorted_array) - 1:
        difference = found_number_index + bias - (len(sorted_array) - 1)
        result = 0 + difference - 1
        print(f'\nЗначение {searching_number} находится в спике {array} под индексом {result}.')
    else:
        result = found_number_index + bias
        print(f'\nЗначение {searching_number} находится в спике {array} под индексом {result}.')


def menu_show ():
    print(
        '\n'
        '1. Вычислить значение синуса;',
        '2. Вычислить значение косинуса;',
        '3. Сколько Маше нужно времени, чтобы накопить?',
        '4. Ряд Фибоначчи;',
        '5. Найти минимальный, максимальный элемент и сумму всех;',
        '6. Найти повторы в списке;',
        '7. Бинарный поиск;',
        '8. Бинарный поиск со смещением;',
        '9. Завершить.\n',
        sep='\n'
    )


if __name__ == "__main__":
    flag = False
    while not flag:
        menu_show()
        try:
            choice = int(input('Выш выбор: '))
        except:
            print('Вы ввели не число.')
            continue
        if 1 > choice > 9:
            print('Такого значение нет.')
        match choice:
            case 1:
                isSin = True
                sin_cos(isSin)
            case 2:
                isSin = False
                sin_cos(isSin)
            case 3:
                money_saver()
            case 4:
                fibonacci_series()
            case 5:
                sum_min_max()
            case 6:
                find_reps()
            case 7:
                binary_search()
            case 8:
                binary_search_with_bias()
            case 9:
                flag = True