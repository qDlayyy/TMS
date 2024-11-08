import random

############ Функции ИКТ ############
def BMI_params_determination(text_tuple):
    while True:
        try:
            param = float(input(f'Введите {text_tuple[0]} в {text_tuple[1]}: '))
            if param <= 0:
                raise Exception(f'{text_tuple[0].capitalize()} не может быть {param}.')
            else: break
        except ValueError as error:
            print(f'Ошибка при вводе параметра "{text_tuple[0]}".')
            continue
        except Exception as error:
            print(f"Ошибка: {error}")
            continue

    return param


def BMI_calculator(height, weight):

    return round(weight / height ** 2, 2)


def BMI_on_result_conclusion(BMI):

    if BMI <= 16:
        conclusion = 'Выраженный дефицит массы тела.'
    elif BMI < 18.5:
        conclusion = 'Недостаточная (дефицит) масса тела.'
    elif BMI < 25:
        conclusion = 'Норма.'
    elif BMI < 30:
        conclusion = 'Избыточная масса тела (предожирение).'
    elif BMI < 35:
        conclusion = 'Ожирение первой степени.'
    elif BMI < 40:
        conclusion = 'Ожирение второй степени.'
    else:
        conclusion = 'Ожирение третьей степени (морбидное).'

    return conclusion


def BMI():
    try:
        height = BMI_params_determination(('рост', 'см'))
        height /= 100
        weight = BMI_params_determination(('Вес', 'кг'))

        BMI_result = BMI_calculator(height, weight)
        BMI_conclusion = BMI_on_result_conclusion(BMI_result)

        print(f'\nИндекс массы тела составляет: {BMI_result} Вывод: {BMI_conclusion}')

    except Exception as error:
       print(str(error))


############ Функции калькулятора ############
def input_determination():
    while True:
        try:
            number = float(input('Введите первое число: '))
            break
        except:
            print(f'Вы ввели не число.')
            continue
    return number


def operation_determination():
    array_of_operations = ['+', '-', '*', '/', '//', '%']
    while True:
        try:
            operation = str(input('Введите операцию: '))
            if operation not in array_of_operations:
                raise TypeError('Неверно введена операция.')
            else:
                break
        except Exception as error:
            print(error)
            continue
    return operation


def isNotZero(number):
    if number == 0:
        raise ZeroDivisionError('Второй операнд не может быть равен 0 при делении и делении нацело.')
    else:
        pass


def isNotInteger(number):
     if not isinstance(number, int):
         raise ValueError('Минимум один из операндов является не целым числом. Нельзя выполнить деление нацело или найти остаток от деления.')
     else: pass


def calculation_zone(operand_one, operand_two, operation):
    if operation in ['%', '/', '//']:
        isNotZero(operand_two)

    if operation in ['//', '%']:
        isNotInteger(operand_one)
        isNotInteger(operand_two)

    result = 0
    match operation:
        case '+':
            result = operand_one + operand_two
        case '-':
            result = operand_one - operand_two
        case '/':
            result = operand_one / operand_two
        case '*':
            result = operand_one * operand_two
        case '//':
            result = operand_one // operand_two
        case '%':
            result = operand_one % operand_two

    return result


def calculator():
    """
    Для тестирования калькулятора создал небольшую функцию с использованием assert. В функции menu() -> case 2 можно
    снять комментарии и запустить через меню этот пункт. Тест работает через рандом и выведет ошибки теста
    (если ошибка в вычислении моего калькулятора), обработанные(например, при делении я поднимаю ошибку ZeroDivisionError
     с измененным сообщением), необработанные(если возникнет ошибка, которая не была мной обработана и должна была
     сломать программу, но была поймана).
    """
    try:
        operand_one = input_determination()
        operand_two = input_determination()
        operation = operation_determination()

        result = calculation_zone(operand_one, operand_two, operation)
        print(f'\nРезультат выражения {operand_one} {operation} {operand_two} = {result}')

    except ZeroDivisionError as error:
        print(error)
    except ValueError as error:
        print(error)
    except:
        print('Произошла какая-то другая ошибка.')


def calculator_small_tests():
    """
    Самому проверять работу калькулятора долго. Можно написать небольшой тест с использованием assert и try-except конструкции.
    Создаем список как из целых чисел(для определенных операций), так и дробных. Числа берем как отрицательные, так и положительные.
    Добавляем 0, чтобы проверить поднятую ошибку при делении на 0. Создаем блоки по равному количеству тестов на операцию.
    Для операций, где ошибки не поднимались намеренно проверяем лишь правильность операции. Для %, / и // перед тем как
    проверить правильность вычислений надо проверить поднялась ли ошибка (если требуется). Поскольку в самой функции
    calculator_zone обработчика ошибок нет, то поднятые там ошибки выйдут за функцию. Поэтому обработчик тестов их словит.
    Они будут считаться такими же ошибками, но выводиться будут с измененным сообщением. Таким образом их можно будет
    отличить от необработанных ошибок(которые просто были пойманы, но не ожидались) и ошибок assert. Если ошибки не появились,
    то проводится тестирование правильности подсчтета. Выводятся лишь обработанные ошибки, необработанные ошибки и ошибки
    подсчета. Правильно посчитанные выражения без поднятых намеренно ошибок не выводятся.
    """
    try:
        list_of_test_nums = [random.randint(-100,100) for _ in range(10)] + [random.uniform(-100.0, 100.0) for _ in range(10)]
        list_of_test_nums.append(0)
        random.shuffle(list_of_test_nums)
        for test in range(120):
            try:
                if test < 20:
                    operand_one = list_of_test_nums[random.randint(0,20)]
                    operand_two = list_of_test_nums[random.randint(0,20)]
                    operation = '+'
                    assert (calculation_zone(operand_one, operand_two, operation) == operand_one + operand_two)
                elif test < 40:
                    operand_one = list_of_test_nums[random.randint(0, 20)]
                    operand_two = list_of_test_nums[random.randint(0, 20)]
                    operation = '-'
                    assert (calculation_zone(operand_one, operand_two, operation) == operand_one - operand_two)
                elif test < 60:
                    operand_one = list_of_test_nums[random.randint(0, 20)]
                    operand_two = list_of_test_nums[random.randint(0, 20)]
                    operation = '*'
                    assert (calculation_zone(operand_one, operand_two, operation) == operand_one * operand_two)
                elif test < 80:
                    operand_one = list_of_test_nums[random.randint(0, 20)]
                    operand_two = list_of_test_nums[random.randint(0, 20)]
                    operation = '/'
                    calculation_zone(operand_one, operand_two, operation)
                    assert (calculation_zone(operand_one, operand_two, operation) == operand_one / operand_two)
                elif test < 100:
                    operand_one = list_of_test_nums[random.randint(0, 20)]
                    operand_two = list_of_test_nums[random.randint(0, 20)]
                    operation = '//'
                    calculation_zone(operand_one, operand_two, operation)
                    assert (calculation_zone(operand_one, operand_two, operation) == operand_one // operand_two)
                else:
                    operand_one = list_of_test_nums[random.randint(0, 20)]
                    operand_two = list_of_test_nums[random.randint(0, 20)]
                    operation = '%'
                    calculation_zone(operand_one, operand_two, operation)
                    assert (calculation_zone(operand_one, operand_two, operation) == operand_one % operand_two)

            except AssertionError:
                print(f'Ошибка в тесте {test}: {operand_one} {operation} {operand_two}\n')

            except ZeroDivisionError as error:
                print(f'\nОбработанная ошибка: {error}\n'
                      f'Ошибка в тесте {test}: {operand_one} {operation} {operand_two}\n')

            except ValueError as error:
                print(f'\nОбработанная ошибка: {error}\n'
                      f'Ошибка в тесте {test}: {operand_one} {operation} {operand_two}\n')

    except TypeError as error:
        print(f'{error}: Ошибка создания списка.')
    except Exception as error:
        print(f"Необработанная ошибка: {error}")

    finally:
        print("Тесты завершены.")


############ Сервисные функции ############
def menu():
    menu = '\n1. Посчитать ИМТ;\n' \
           '2. Калькулятор;\n' \
           '3. Завершить.'
    while True:
        try:
            choice = int(input(f'{menu}\n\nВыберите пункт: '))
            if choice not in range(1,4):
                raise IndexError('Такого пункта не существует.')
            else: pass
        except ValueError:
            print('Вы ввели не целое число.')
            continue
        except Exception as error:
            print(f'Ошибка: {error}')

        match choice:
            case 1:
                BMI()
            case 2:
                calculator()
                # calculator_small_tests()
            case 3:
                return False


if __name__ == '__main__':
    menu()

