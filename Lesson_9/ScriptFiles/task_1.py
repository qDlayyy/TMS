import os
import re
import random


def minor_tasks_info():
    os_name = os.name
    current_directory = os.getcwd()

    return os_name, current_directory


def random_files_creation(path_to_directory, file_amount):
    list_of_expansions = ['.txt', '.xml', '.pdf', '.csv', '.json']
    list_of_files_to_create = []

    for iter in range(file_amount):
        random_number = random.randint(0, len(list_of_expansions) - 1)
        expansion = list_of_expansions[random_number]
        list_of_files_to_create.append(f'{str(random.randint(0, 1000))}{expansion}')

    os.makedirs(path_to_directory, exist_ok=True)

    for file_name in list_of_files_to_create:
        file_path = os.path.join(path_to_directory, file_name)
        with open(file_path, 'w') as file:
            for line_index in range(0, random.randint(0, 10)):
                file.write(f'{str(random.randint(10000, 9999999))*random.randint(0, 7)}\n')


def file_sorting(directory):

    path = os.path.join(directory)

    if not (os.path.isdir(path) and len(os.listdir(path))):
        print('\nFolder is empty. Filling them.')
        file_amount = 7
        random_files_creation(directory, file_amount)
        print(f'\n{file_amount} files have been created.')
        print(f'Created files: {os.listdir(directory)}\n')

    file_distribution_control = {}

    parent_directory = os.path.dirname(directory)
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        if not os.path.isfile(file_path):
            continue

        name, extension = os.path.splitext(file_name)
        no_dot_extension = extension.split('.')[1]

        if not file_distribution_control.get(no_dot_extension):
            file_distribution_control[no_dot_extension] = os.path.getsize(file_path)
        else:
            file_distribution_control[no_dot_extension] += os.path.getsize(file_path)


        new_path = os.path.join(parent_directory, no_dot_extension)
        os.makedirs(new_path, exist_ok=True)
        new_file_path = os.path.join(new_path, file_name)
        os.rename(file_path, new_file_path)

        print(f'File {file_name} has been successfully moved to {no_dot_extension}.')

    keys = list(file_distribution_control.keys())
    line = '\n'
    for key in keys:
        line += f'Files moved to {key} have overall size of {file_distribution_control[key]} bites. \n'

    print(line)

    file_name_changer(parent_directory)


def string_input_check(text_to_show):
    while True:
        try:
            string_input = input(text_to_show)
            break
        except:
            print('It seems to be not even a string. Try again.')

    return string_input


def file_name_changer(parent_directory):
    while True:
        try:
            for directory in os.listdir(parent_directory):
                if directory != 'AllFilesHolder': print(f'### {directory}')
            try:
                chosen_directory = input("\nLet's rename any of the documents. Choose the directory first: ")
                chosen_directory = chosen_directory.strip()

                if not os.path.isdir(os.path.join(parent_directory, chosen_directory)):
                    raise Exception('There is no such directory. Try again.\n')
                else: break


            except ValueError:
                print('It seems to be not even the name of any directory. Try again.')
                continue

        except Exception as error:
            print(error)
            continue

    chosen_directory_path = os.path.join(parent_directory, chosen_directory)

    for file in os.listdir(chosen_directory_path):
        print(f'### {file}')

    while True:
        file_name = string_input_check('\nWhat file to choose: ')
        file_path = os.path.join(chosen_directory_path, file_name)
        if not os.path.isfile(file_path):
            print('There is no such file in chosen directory. Try again.')
            continue
        else: break

    while True:

        new_file_name = string_input_check('\nEnter new file name. Please use previous extension in order not to damage the file: ')
        new_file_name = new_file_name.strip()
        name, extension = os.path.splitext(file_name)
        extension = extension[1:]
        filename_regex = rf'[a-zA-Z0-9_]+(?:\s*[.-]\s*[a-zA-Z0-9_]+)*\.{extension}'

        if not re.match(filename_regex, new_file_name):
            print('You cannot name the file like that. Try again.')
            continue
        else: break

    new_file_path = os.path.join(chosen_directory_path, new_file_name)
    if os.path.isfile(new_file_path):
        print('\nThe name you entered is currently being used. Old file will be overwritten.')

    os.rename(file_path, new_file_path)
    print(f'File {os.path.basename(file_path)} has been successfully moved to a new directory {os.path.basename(new_file_path)}.\n')