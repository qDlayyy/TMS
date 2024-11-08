import re
from functools import reduce


def file_reader(relative_path):
    try:
        with open(relative_path, 'r') as file:
            array_of_file = file.readlines()
    except Exception as error:
        print(error)

    text = reduce(lambda prev_line, next_line: prev_line + next_line, map(lambda line: line.split('\n')[0], array_of_file))

    return text


def text_changing_by_pattern(pattern, text, replacement):
    new_text = re.sub(pattern, replacement, text)

    return new_text


def new_full_name_determination(full_name_pattern):
    full_name = None
    while True:
        try:
           full_name = str(input('\nEnter full name of accused: '))
           if not re.match(full_name_pattern, full_name):
               raise Exception
           else: break

        except:
            print('You have entered incorrect full name. Try again. Use the language of the text.')
            continue

    return full_name


def court_task(directory):
    full_name_pattern = r'[А-Я][а-я]+-?[А-Я]?[а-я]+\s[А-Я][а-я]+\s[А-Я][а-я]+'
    text = file_reader(directory)
    print(f'\nOriginal text: \n{text}')
    replacement = new_full_name_determination(full_name_pattern)
    replaced_text = text_changing_by_pattern(pattern=full_name_pattern, text=text, replacement=replacement)
    print(f'\nChanged text: \n{replaced_text}\n')