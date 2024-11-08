import os.path
import re
from functools import reduce


def file_reader(directory):
    file_path = os.path.join(directory)

    if not os.path.isfile(file_path):
        raise Exception('\nError. No such file. Check your directory or file existence.\n')

    with open(file_path, 'r') as text_file:
        list_of_lines = list(map(lambda line: line.strip(), text_file.readlines()))

    return list_of_lines


def numbers_in_text_search(list_of_lines):
    regex_pattern = r'\d+\.\d+|\d+'
    list_of_regex_matches = []

    if list_of_lines == []:
        raise Exception("\nYou haven't provided with any text. No text means no result.\n")

    print('\nThe text from your file: ')
    for line in list_of_lines:
        print(line)
        list_of_regex_matches.append(re.findall(regex_pattern, line))

    list_of_lists_with_numbers = []
    for inner_list in list_of_regex_matches:
        inner_list = list(map(lambda item: float(item), inner_list))
        list_of_lists_with_numbers.append(inner_list)

    return list_of_lists_with_numbers


def sum_numbers(list_of_lists_with_numbers):

    result_sum = reduce(lambda prev_list_sum, next_list_sum: prev_list_sum + next_list_sum,
                        map(lambda list: sum(list), list_of_lists_with_numbers))

    return result_sum


def numbers_search(directory):
    try:
        list_of_lines = file_reader(directory)
        list_of_lists_with_numbers = numbers_in_text_search(list_of_lines)
        result_sum = sum_numbers(list_of_lists_with_numbers)

        print(f'\nThe sum of numbers in the text is {result_sum}.\n') if result_sum > 0 else \
            print('\nNo numbers have been found in your text.\n')

    except Exception as error:
        print(error)
