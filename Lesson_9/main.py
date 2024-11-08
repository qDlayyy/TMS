from ScriptFiles.task_1 import file_sorting, minor_tasks_info
from ScriptFiles.task_2 import court_task
from ScriptFiles.task_3 import file_lines_reader, file_words_counter
from ScriptFiles.task_4 import file_banned_words_changer
from ScriptFiles.task_5 import bad_students_determination
from ScriptFiles.task_6 import numbers_search
from ScriptFiles.task_7 import Caesars_cipher
from ScriptFiles.task_8 import json_csv_main, json_scv_loop


def T1_file_work():
    # random_files_creation('./Task_1/AllFilesHolder', 5)
    directory = './Task_1/AllFilesHolder'
    os_name, current_directory = minor_tasks_info()
    print(f'OS name: {os_name}.')
    print(f'Current directory path: {current_directory}.')
    file_sorting(directory)


def T2_court_judgment():
    directory = './Task_2/court_file.txt'
    court_task(directory)


def T3_most_common_word():
    directory = './Task_3/textHolder.txt'
    file_words_counter(directory)


def T4_banned_words_changer():
    directory = './Task_4'
    file_banned_words_changer(directory)


def T5_bad_students_determination():
    directory = './Task_5/students.txt'
    bad_students_determination(directory)


def T6_numbers_i_text_search():
    directory = './Task_6/text.txt'
    numbers_search(directory)


def T7_Caesars_cipher():
    directory = './Task_7/text.txt'
    Caesars_cipher(directory)


def T8_json_csv():
    directory = './Task_8/data.json'
    json_scv_loop(directory)


def menu():
    menu = ['1. Files;', '2. Court perpetrator change;', '3. Most common word per line;',
            '4. Banned words changer;', '5. Bad students determination;', '6. Numbers in text search;',
            '7. Caesar\'s cipher;', '8. Json & CSV', '9. Finish.' ]
    choice_request = '\nChose the point: '
    while True:
        while True:
            list(map(lambda menu_point: print(menu_point), menu))
            try:
                choice = int(input(choice_request))
                if choice <= 0 or choice > len(menu):
                    raise Exception('Incorrect point. Try another one.\n')
                else: break
            except ValueError:
                print('You have entered not a number. Try again.\n')
            except Exception as error:
                print(error)

        match choice:
            case 1:
                T1_file_work()
            case 2:
                T2_court_judgment()
            case 3:
                T3_most_common_word()
            case 4:
                T4_banned_words_changer()
            case 5:
                T5_bad_students_determination()
            case 6:
                T6_numbers_i_text_search()
            case 7:
                T7_Caesars_cipher()
            case 8:
                T8_json_csv()
            case 9:
                return False


if __name__ == '__main__':
    menu()