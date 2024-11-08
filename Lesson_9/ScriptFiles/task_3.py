import os
import re
from collections import Counter

def file_lines_reader(directory):
    file_path = os.path.join(directory)

    try:
        with open(file_path, 'r') as file:
            list_of_lines = file.readlines()

    except:
        print('There is no such file. Try again.')
        return None

    list_of_lines = list(map(lambda line: line.strip(), list_of_lines))

    list_of_result = []
    for line in list_of_lines:
        words = line.split(' ')
        words = list(map(lambda word: word.lower(), words))

        if not words:
            list_of_result.append(None)
            continue

        word_counts = Counter(words)
        most_common = word_counts.most_common(1)
        list_of_result.append(most_common)

    return list_of_result


def new_file_result_writer(directory, file_name, list_of_result):
    new_file_path = os.path.join(os.path.dirname(directory), file_name)

    if os.path.isfile(new_file_path):
        print(f'File {os.path.basename(new_file_path)} exists and will be overwritten.')

    with open(new_file_path, 'a') as file:
        file.write(f'Words counter per line for file {os.path.basename(directory)}\n\n')

        for line_id, result in enumerate(list_of_result):
            word, amount = result[0]

            if word:
                file.write(f'The most common word in line {line_id + 1} is "{word}". It occurs {amount} times.\n')
            else:
                file.write(f'The line {line_id} seems to be empty.\n')

    print(f'File name {file_name} has been successfully created and filled.\n')


def string_input_check(text_to_show):
    while True:
        try:
            string_input = input(text_to_show)
            break

        except:
            print("It doesn't look like a string. Try again.")

    return string_input


def new_file_name_determination(file_name_pattern):
    while True:
        try:
            file_name = string_input_check('\nWhat is the file name you want to create for the answer: ')
            if not re.match(file_name_pattern, file_name):
                raise Exception('You cannot name new file like that. Try again.')
            else: break

        except Exception as error:
            print(error)

    return file_name


def file_words_counter(directory):
    file_name_pattern = rf'[a-zA-Z0-9_]+(?:\s*[.-]\s*[a-zA-Z0-9_]+)*\.txt'
    list_of_results = file_lines_reader(directory)
    file_name_for_results = new_file_name_determination(file_name_pattern)
    new_file_result_writer(directory,  file_name_for_results, list_of_results)