import os
import json
import csv
import re


def json_csv_main(directory):
    try:
        data = json_reader(directory)
        csv_file_creation_text = '\nName your CSV file: '
        file_name = file_name_check(csv_file_creation_text, 'csv')
        to_csv_converter(data, directory, file_name)

    except Exception as error:
        print(error)


def json_reader(directory):
    file_path = os.path.join(directory)

    if not os.path.isfile(file_path):
        raise Exception('Error. No such file. Check your directory and file existence.')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    return data


def file_name_check(text, extension):
    file_name_pattern = rf'[a-zA-Z0-9_]+(?:\s*[.-]\s*[a-zA-Z0-9_]+)*\.{extension}'
    while True:
        try:
            file_name = input(text)

            if not re.match(file_name_pattern, file_name):
                print('You cannot name your file like that.')
                continue
            else:
                break

        except ValueError:
            print("It's not even a string.")
        except Exception as error:
            print(error)

    return file_name


def file_existence_check(directory):
    directory = os.path.dirname(directory)
    while True:
        for file in os.listdir(directory):
            print(f'### {file}')
        try:
            file_name = file_name_check('\nWhat file do you chose? ', 'csv')
            file_path = os.path.join(directory, file_name)

            if not os.path.isfile(file_path):
                raise Exception('No such file.')
            else:
                break
        except Exception as error:
            print(error)

    return file_name


def to_csv_converter(data, directory, file_name):

    file_path = os.path.join(os.path.dirname(directory), file_name)

    with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
        headers = list(data[0].keys())
        writer = csv.DictWriter(csv_file, fieldnames=headers)

        writer.writeheader()

        for person in data:
            person['languages'] = ', '.join(person['languages'])
            writer.writerow(person)

    print(f'\nFile {file_name} has been successfully created and loaded.')


def new_data_creation(data):
    keys = list(data[0].keys())

    new_employee = {}
    for key in keys:
        if key != 'languages' and key != 'car':
            string = input_correction_check(case=key, text=f'What is your {key}? ')
        elif key == 'car':
            answer = input_range_check(f'Do you have a {key}? ', 1, 2)
            if answer == 1:
                string = True
            else:
                string = False
        else:
            amount = int_input_check('How many languages do you know? ')
            list_of_languages = list_of_languages_determination(amount)
            string = list_of_languages

        new_employee[key] = string

    return new_employee


def list_of_languages_determination(amount):
    list_of_languages = []
    if not amount:
        return ''

    for language in range(amount):
        text = f'What is language #{language + 1}: '
        string = input_correction_check('language', text)
        list_of_languages.append(string)

    return list_of_languages


def int_input_check(text):
    while True:
        try:
            num = int(input(text))
            if num < 0:
                return None
            break
        except:
            print('It is not even a number. Try again.')

    return num


def input_range_check(text, min, max):
    while True:
        try:
            choice = int(input(f'{text} \n1. Yes \n2. No \nYour answer: '))
            if choice < min or choice > max:
                raise Exception('Incorrect choice. Try again.')
            else: break

        except ValueError:
            print('It is not even a number.')
        except Exception as error:
            print(error)

    return choice


def input_correction_check(case, text):
    name_pattern = r"[A-Za-zА-ЯЁ][a-zа-яёA-ZА-ЯЁ\s'-]*"
    date_pattern = r"(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(\d{4})"

    if case == 'name':
        pattern = name_pattern
    elif case == 'birthday':
        pattern = date_pattern
    else:
        pattern = None

    while True:
        try:
            string = input(text)

            if pattern and not re.match(pattern, string):
                raise Exception('I cannot access this data. Try again.')
            else: break

        except ValueError:
            print(ValueError)
        except Exception as error:
            print(error)

    return string


def json_add(directory, new_data):

    data = json_reader(directory)
    data.append(new_data)

    file_path = os.path.join(directory)

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print('\nNew employee was successfully added to a json file.\n')


def csv_add(directory_to_file, new_data):
    file_path = os.path.join(directory_to_file)

    with open(file_path, 'a', newline='', encoding='utf-8') as csv_file:
        headers = list(new_data.keys())
        writer = csv.DictWriter(csv_file, fieldnames=headers)

        csv_file.seek(0, 2)
        if csv_file.tell() == 0:
            writer.writeheader()

        writer.writerow(new_data)

    print('\nNew employee was successfully added to a csv file.\n')


def json_search(directory, key_name, key_param):
    data = json_reader(directory)

    for employee in data:
        if employee[key_name] == key_param:
            return employee

    return None


def json_search_many(directory, key_name, key_param):
    data = json_reader(directory)

    if key_name == 'languages':
        list_of_employees = []
        for employee in data:
            if key_param in employee[key_name]:
                list_of_employees.append(employee)

        if list_of_employees:
            return list_of_employees

    elif key_name == 'birthday':
        list_of_employees = []
        for employee in data:
            if int(key_param) >= int(employee[key_name].split('.')[-1]):
                list_of_employees.append(employee)

        if list_of_employees:
            return list_of_employees

    return None


def average_year(list_of_employees):
    year_sum = 0
    for employee in list_of_employees:
        year_sum += int(employee['birthday'].split('.')[-1])

    result = year_sum / len(list_of_employees)

    return result


def data_show(data):
    if data:
        keys = list(data.keys())

        print(f'\nFound information: ')
        for key in keys:
            print(f'{key}: {data[key]}')
        print()
    else:
        print('\nThere is no such employee. Check if you wrote searching parameter correctly.\n')


def T8_T1_json_reader(directory):
    data = json_reader(directory)
    for person in data:
        data_show(person)


def T8_T2_json_to_csv(directory):
    data = json_reader(directory)
    csv_file_creation_text = '\nName your CSV file: '
    file_name = file_name_check(csv_file_creation_text, 'csv')
    to_csv_converter(data, directory, file_name)


def T8_T3_json_add(directory):
    data = json_reader(directory)
    new_data = new_data_creation(data)
    json_add(directory, new_data)


def T8_T4_csv_add(directory):
    file_name = file_existence_check(directory)
    directory_to_csv_file = os.path.join(os.path.dirname(directory), file_name)
    data = json_reader(directory)
    new_data = new_data_creation(data)
    csv_add(directory_to_csv_file, new_data)


def T8_T5_info_for_name(directory):
    name = input_correction_check('name', 'Who you want to check? ')
    found_data = json_search(directory, 'name', name)
    data_show(found_data)


def T8_T6_language_search(directory):
    language = input_correction_check('languages', 'What language are we looking for? ')
    found_data = json_search_many(directory, 'languages', language)

    if found_data:
        for data in found_data:
            data_show(data)
    else:
        data_show(None)


def T8_T7_below_year_search(directory):
    year = input_correction_check('year', 'What is the the biggest year of birth? ')
    found_data = json_search_many(directory, 'birthday', year)

    if found_data:
        for data in found_data:
            data_show(data)
        result = average_year(found_data)
        print(f'Average birth year among employees under {year} is {result:.2f}.\n')
    else:
        data_show(None)


def json_csv_menu(directory):
    menu = ['\n1. Json reader;', '2. Json to CSV;', '3. Json add;', '4. CSV add;', '5. Found employee by name;',
            '6. Found employee by language;', '7. Found employees by year;', '8. Finish with Json & CSV.']
    choice_request = '\nChose the point: '
    while True:
        while True:
            list(map(lambda menu_point: print(menu_point), menu))
            try:
                choice = int(input(choice_request))
                if choice <= 0 or choice > len(menu):
                    raise Exception('Incorrect point. Try another one.\n')
                else:
                    break
            except ValueError:
                print('You have entered not a number. Try again.\n')
            except Exception as error:
                print(error)

        match choice:
            case 1:
                T8_T1_json_reader(directory)
            case 2:
                T8_T2_json_to_csv(directory)
            case 3:
                T8_T3_json_add(directory)
            case 4:
                T8_T4_csv_add(directory)
            case 5:
                T8_T5_info_for_name(directory)
            case 6:
                T8_T6_language_search(directory)
            case 7:
                T8_T7_below_year_search(directory)
            case 8:
                return False


def json_scv_loop(directory):
    json_csv_menu(directory)
