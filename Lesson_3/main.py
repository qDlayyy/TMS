
'''Каждая функция содержит в себе решение одной задачи из презентации. Я рассмотрел не только решение задач, но и
    некоторые исключения, которые приходят в голову при тестировании функций. Функции вызываются в порядке очереди
    по презентации. Каждая из них принимает на вход переменные, требуемые по задаче, прозводит минимальные
    проверки и решает задачу.'''


def number_operations(num1, num2, num3):
    if isinstance(num1, int) and isinstance(num2, int) and isinstance(num3, int):
        sum = num1 + num2 + num3
        difference = num1 - num2 - num3
        multiplication = num1 * num2 * num3
        dif_and_sum = num1 - num2 + num3
        mult_and_div = num1 * num2 / num3
        rem = (num1 + num2) % num3
        print(f'Сумма: {sum}', f'Вычитание: {difference}', f'Умножение: {multiplication}',
              f'Вычитание и сумма: {dif_and_sum}',
              f'Умножение и деление: {mult_and_div}', f'Остаток от суммы: {rem}', sep=';\n')
    else:
        print('Вы ввели не три целых числа.')


def area_of_triangle (cat_a, cat_b):
    area = cat_a*cat_b*0.5
    hypotenuse = round((cat_a ** 2 + cat_b ** 2) ** 0.5, 2)
    print(f'Площадь треугольника: {area}')
    print(f'Гипотенуза треугольника: {hypotenuse}')


def word_counter (string):
    if string.strip():
        print(f'Количество слов: {len(string.split(" "))}')
    else:
        print('Вы ввели пустую строку.')


def char_replacement(string):
    first_char = string.find('h')
    last_char = string.rfind('h')
    if first_char == -1 or first_char == last_char:
        print('Здесь только одно вхождение или их нет вовсе')
    else:
        prev_line = string[:first_char + 1]
        middle_line = string[first_char + 1: last_char]
        end_line = string[last_char:]
        new_line = middle_line.replace('h', 'H')
        print(f'Старая строка: {string}')
        print(f'Новая строка: {prev_line + new_line + end_line}')


def string_changing(string):
    the_third_char = string[2]
    pre_last_char = string[-2]
    first_five_chars = string[:5]
    all_chars_except_last_two = string[:-2]
    only_even_chars = string[::2]
    only_odd_chars = string[1::2]
    reversed_string = string[::-1]
    reversed_odd_string = string[::-1][::2]
    string_length = len(string)
    print(
        f'1. {the_third_char}',
        f'2. {pre_last_char}',
        f'3. {first_five_chars}',
        f'4. {all_chars_except_last_two}',
        f'5. {only_even_chars}',
        f'6. {only_odd_chars}',
        f'7. {reversed_string}',
        f'8. {reversed_odd_string}',
        f'9. {string_length}',
        sep=';\n'
    )


def units_shower(number):
    if type(number) == int:
        print(f'Последняя цифра числа {number}: {number % 10}')
    else:
        print('Это не целое число.')


def tens_shower(number):
    if type(number) != int or len(str(number)) != 3:
        print('Это не трехзначное число.')
    else:
        print(f'Количество десятков в числе {number}: {abs(number) // 10 % 10}')


def digit_counter(number):
    if type(number) != int or len(str(number)) != 3:
        print('Это не трехзначное число.')
    else:
        absed_number = abs(number)
        hundreds = (absed_number // 100)
        tens = absed_number // 10 % 10
        units = absed_number % 10
        result = hundreds + tens + units
        print(f'Результатом сложения цифр числа {number}: {result}')



if __name__ == '__main__':
    print('Задание №1')
    number_operations(1, 2, 4)

    print('\nЗадание №2')
    area_of_triangle(3, 4)

    print('\nЗадание №3')
    word_counter('Здесь ответ должен быть 5')

    print('\nЗадание №4')
    char_replacement('aHsdhHgggtehsahHdsahf')

    print('\nЗадание№5')
    string_changing('TEST-STR')

    print('\nЗадание №6')
    units_shower(121)

    print('\nЗадание №7')
    tens_shower(384)

    print('\nЗадание №8')
    digit_counter(896)