import random
from functools import reduce
from math import inf


def columns_and_rows_determination():
    while True:
        try:
            rows = int(input('Введите количество строк(M): '))
            columns = int(input('Введите количество колонок(N): '))
            if columns <= 0 or rows <= 0:
                print('Вы не можете создать матрицу с таким количеством строк и колонок.')
                continue

            break
        except:
            print('Вы ввели значение, которое не является целым.')
            continue
    return columns, rows


def matrix_creation(columns_M, rows_N, random_tuple):
    matrix = []
    for row in range(rows_N):
        new_row = []
        for item in range(columns_M):
            new_row.append(random.randint(random_tuple[0], random_tuple[1]))
        matrix.append(new_row)
    return matrix


def matrix_show(matrix, message: ''):
    max_width = max(len(str(item)) for row in matrix for item in row)
    print(f'\n{message}')
    for row in matrix:
        print(" | ".join(f"{value: >{max_width}}" for value in row))


def min_max_in_matrix(matrix):
    min_value = inf
    max_value = -inf

    for row in matrix:
        min_value = min(row) if min(row) < min_value else min_value
        max_value = max(row) if max(row) > max_value else max_value

    return min_value, max_value


def matrix_elements_sum(matrix):
    elements_sum = 0
    for row in matrix:
        elements_sum += sum(row)
    print(f'\nСумма элементов всей матрицы равна: {elements_sum}')
    return elements_sum


def elements_in_column_sum(matrix):
    columns_amount = len(matrix[0])
    array_with_element_per_column = [0] * columns_amount
    for row in matrix:
        for id, element in enumerate(row):
            array_with_element_per_column[id] += element

    return array_with_element_per_column


def column_sum_percentage(matrix_elements_sum, array_with_sum_per_column):

    for id, column_sum in enumerate(array_with_sum_per_column):
        percentage = column_sum / matrix_elements_sum
        print(f'Колонна №{id + 1} -> {column_sum} -> {percentage:.2%}')


def matrix_column_determination(matrix):
    while True:
        try:
            column_number = int(input('\nВыберите колонну (начиная с 1): '))
            if column_number <= 0 or column_number > len(matrix[0]):
                print('Вы вышли за предел.')
                continue
            else: break

        except:
            print('Такой колонны не существует.')
            continue
    return column_number - 1


def matrix_column_choice_return(matrix, choice):
    rowed_matrix = []
    for row in matrix:
        rowed_matrix.append(row[choice])

    k_matrix = []
    for row in rowed_matrix:
        new_row = []
        for column in range(1):
            new_row.append(row)
        k_matrix.append(new_row)

    return k_matrix


def k_matrix_multiplication(matrix, k_matrix):
    new_matrix = []
    for row_id, row in enumerate(matrix):
        new_row = []
        for element in row:
            new_row.append(element * k_matrix[row_id][0])
        new_matrix.append(new_row)

    return new_matrix


def k_column_inner_multiplication(k_matrix):
    inner_multiplication = 1
    for row in k_matrix:
        inner_multiplication *= row[0]

    return inner_multiplication


def matrix_row_determination(matrix):
    while True:
        try:
            row_number = int(input('\nВыберите ряд (начиная с 1): '))
            if row_number <= 0 or row_number > len(matrix):
                print('Вы вышли за предел.')
                continue
            else: break

        except:
            print('Такого ряда не существует.')
            continue
    return row_number - 1


def matrix_row_choice_return(matrix, row_number):

    return matrix[row_number]


def l_row_matrix_sum(matrix, l_row):
    new_matrix = []
    for row in matrix:
        new_row = []
        for element_id, element in enumerate(row):
            new_row.append(element + l_row[element_id])
        new_matrix.append(new_row)

    return new_matrix


def l_row_inner_sum(l_row):
    return sum(l_row)


def searching_number_determination():
    while True:
        try:
            target_value = int(input('\nВведите число, которое нужно найти в матрице: '))
            break
        except:
            print('Вы ввели некорректное значение.')
            continue

    return target_value


def searching_for_number_in_matrix(matrix, target_value):
    column_amount = len(matrix[0]) - 1
    possible_column_ids = list(integer_generator(column_amount))
    array_isIn = [False] * (column_amount + 1)
    while possible_column_ids != []:
        for row in matrix:
            for array_id, column_id in enumerate(possible_column_ids):
                if row[column_id] == target_value:
                    array_isIn[column_id] = True
                    possible_column_ids[array_id] = None
            while None in possible_column_ids:
                possible_column_ids.remove(None)
        break

    print("")
    for id, boolean in enumerate(array_isIn):
        print(f'Столбец №{id + 1} -> {"содержит" if boolean else "не содержит"} значение {target_value}.')


def matrix_diagonal_sum(matrix, isMain):
    current_index = 0
    diagonal_sum = 0
    if isMain:
        for row in matrix:
            diagonal_sum += row[current_index]
            current_index += 1
    else:
        for row_index in range(len(matrix) - 1, -1, -1):
            diagonal_sum += matrix[row_index][current_index]
            current_index += 1

    return diagonal_sum


def matrix_adding_new_column(matrix):
    for row in matrix:
        row.append(0) if row.count(1) % 2 == 0 else row.append(1)


def the_process_of_matrix_creation(range_tuple):
    columns, rows = columns_and_rows_determination()
    matrix = matrix_creation(columns, rows, range_tuple)
    message = f'Матрица {rows}x{columns} имеет вид: '
    matrix_show(matrix, message)

    return matrix


def integer_generator(n):
    for i in range(n + 1):
        yield i
