
def binary_search(array, target_value, left, right):
    if left > right:
        return None

    middle = (left + right) // 2

    if array[middle] == target_value:
        return middle
    elif array[middle] > target_value:
        return binary_search(array, target_value, left, middle - 1)
    else:
        return binary_search(array, target_value, middle + 1, right)


def determination_binary_search():
    while True:
        try:
            array = list(map(int, input('Введите список чисел через пробел: ').split()))
            array.sort()
            break
        except ValueError:
            print('Введите корректный список чисел через пробел.')

    while True:
        try:
            target_value = int(input('Введите искомое число: '))
            break
        except ValueError:
            print('Вы ввели некорректное значение.')

    position = binary_search(array, target_value, 0, len(array) - 1)

    if position is not None:
        line = f'В списке {array} элемент {target_value} находится на позиции {position}.'
    else:
        line = f'В списке {array} элемент {target_value} не найден.'

    return line


##Перевод в бинарную систему
def decimal_determination():
    while True:
        try:
            decimal = int(input('Введите десятичное целое число: '))
            break
        except:
            print('Вы ввели не число.')
            continue

    return decimal


##Определение простое ли число
def isPrime_determination():
    while True:
        try:
            number = int(input('Введите целое число: '))
            if number <= 0:
                print('Простым может быть лишь натуральное число. Это число не является натуральным')
                continue
            else:
                break
        except:
            print('Вы не ввели целое число.')
            continue

    return number


def isPrime(decimal_number):
    decimal_number = abs(decimal_number)

    if decimal_number == 1:
        return False
    elif decimal_number == 2 or decimal_number == 3:
        return True
    elif decimal_number % 2 == 0 or decimal_number % 3 == 0:
        return False

    check_number = 5
    while check_number**2 <= decimal_number:
        if decimal_number % check_number == 0 or decimal_number % (check_number + 2) == 0:
            return False
        check_number += 6
    return True


def decimal_to_binary(decimal):
    if decimal == 0:
        return '0'
    else:
        isPositive = True if decimal > 0 else False
        decimal = abs(decimal)
        binary = ''
        while decimal > 0:
            binary = str(decimal % 2) + binary
            decimal //= 2

    return '0.' + binary if isPositive else '1.' + binary



##Функции нахождения НОД
def greater_common_divisor(number_1, number_2):
    while number_2 != 0:
        number_1, number_2 = number_2, number_1 % number_2
    return number_1


def gcd_determination():
    while True:
        try:
            number_1 = int(input('Введите первое число для нахождения НОД: '))
            number_2 = int(input('Введите второе число для нахождения НОД: '))
            break
        except:
            print('Вы ввели некорректное значение. Попробуйте еще раз')
            continue
    return number_1, number_2
