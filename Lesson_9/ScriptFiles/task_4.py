import os.path
import re


def file_name_determination(directory):
    forbidden_file_path = os.path.join(directory, 'stop_words.txt')
    while True:
        try:
            file_name = input('\nWhat file are we going to check? ')
            file_path = os.path.join(directory, file_name)

            if not os.path.isfile(file_path):
                raise Exception('No such file in accessible directory. Try again.')
            elif file_path == forbidden_file_path:
                raise Exception(f'You cannot choose file {file_name}. Try another file.')
            else:
                break

        except ValueError:
            print("It doesn't look like a string. Try again.")
        except Exception as error:
            print(error)

    return file_path


def directory_show(directory):
    path = os.path.join(directory)

    if os.path.isdir(path):
        print()
        for file in os.listdir(path):
            print(f'### {file}')


def file_reader(file_path):
    print(file_path)
    with open(file_path, 'r') as text_file:
        # list_of_lines = text_file.readlines()
        list_of_lines = list(map(lambda line: line.strip(), text_file.readlines()))

    return list_of_lines


def banned_words(directory):
    path_file = os.path.join(directory)

    with open(path_file, 'r') as banned_file:
        banned_words = (banned_file.readline()).split(' ')

    return banned_words


def words_replacement(match):
    return '*' * len(match.group(0))


def banned_words_search(list_of_text_lines, banned_words):
    """
    Требуется создать паттерн поиска. Для этого мы используем конструкцию, с помощью join по |. Таким образом мы соединяем
    каждой запрещенное слово через логическое или. Используем re.escape для экранирования специальных символов. Благодяря
    этому в тексте можно искать вхождения +, -, /, * и тд. Для замены слова на количество звездочек равное его длине можно
    использовать лямбда-функцию, но тогда вызов re.sub станет невероятно огромным и очевидно менне понятным. Поэтому
    этот функционал был определен внутри маленькой функции. Мы передаем функции без аргументов, хотя по факту они требуются.
    Дело в том, что в случае re.sub функция внутри вызввается автоматически для каждого найденного совпадения match. Мы все еще
    можем передавать аргументы, но это не требуется. Во влаги передаем re.IGNORECASE, чтобы мы производили все выше перечисленные
    действия вне зависимости от регистра.

    """
    banned_words_pattern = rf'\b\w*({"|".join(map(re.escape, banned_words))})\w*\b'
    new_list_of_text = []

    for text in list_of_text_lines:
        new_list_of_text.append(re.sub(banned_words_pattern, words_replacement, text, flags=re.IGNORECASE))

    return new_list_of_text


def text_show(list_of_text):
    line = f'\n{" ".join(list_of_text)}\n'
    print(line)
    return line



def file_banned_words_changer(directory):
    banned_words_file_directory = './Task_4/stop_words.txt'
    directory_show(directory)
    file_path = file_name_determination(directory)
    read_lines = file_reader(file_path)
    list_banned_words = banned_words(banned_words_file_directory)
    list_of_text = banned_words_search(read_lines, list_banned_words)
    text_show(list_of_text)




