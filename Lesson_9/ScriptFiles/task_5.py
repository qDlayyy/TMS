import os

def file_reader(directory):
    file_path = os.path.join(directory)

    if not os.path.isfile(file_path):
        raise Exception('\nError. No such file. Check your directory and file existence.\n')

    with open(file_path, 'r') as students_file:
        map_of_students = map(lambda student: student.strip(), students_file.readlines())

    filtered_students = list(filter(lambda student: int(student.split(' ')[-1]) < 3, map_of_students))

    return filtered_students


def students_show (list_of_students):
    if list_of_students == []:
        print('\nIt seems no students have any marks lower than 3. Check the file it could be empty.\n')
    else:
        print()
        for student in list_of_students:
            name, surname, result = student.split(' ')
            if int(result) >= 0:
                print(f'Student {name} {surname} has mark {result}.')
            else:
                print(f'Well, some of the students are even worse... {name} {surname}. Mark {result}.')
        print()


def bad_students_determination(directory):
    try:
        list_of_bad_students = file_reader(directory)
        students_show(list_of_bad_students)
    except Exception as error:
        print(error)