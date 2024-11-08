import os

def file_reader(directory):
    file_path = os.path.join(directory)

    if not os.path.isfile(file_path):
        raise Exception('\nError. No such file. Check your directory or file existence.\n')

    with open(file_path, 'r') as text_file:
        list_of_text_lines = list(map(lambda line: line.strip(), text_file.readlines()))

    return list_of_text_lines


def cesar_encryption(string, bias, letters):
    main_alphabet_dict = {letter: index + 1 for index, letter in enumerate(letters)}
    additional_alphabet_dict = {index + 1: letter for index, letter in enumerate(letters)}
    letters_limit = len(letters)
    encrypted_string = ''
    for char in string:
        isUpper = True if char.isupper() else False
        if char.isalpha():
            char = char.lower()
            original_position = main_alphabet_dict[char]
            biased_position = original_position + bias

            if biased_position > letters_limit:
                overflow = biased_position - letters_limit
                biased_position = 0
                biased_position += overflow
            else:
                pass

            new_char = additional_alphabet_dict[biased_position]
            if isUpper: new_char = new_char.upper()
            encrypted_string += new_char
        else:
            encrypted_string += char

    return encrypted_string


def encryption_determination(list_of_text_lines):
    alphabet_ru = 'а, б, в, г, д, е, ё, ж, з, и, й, к, л, м, н, о, п, р, с, т, у, ф, х, ц, ч, ш, щ, ъ, ы, ь, э, ю, я'
    letters_ru = alphabet_ru.split(', ')
    alphabet_en = 'a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z'
    letters_en = alphabet_en.split(', ')

    encrypted_list = []
    for line_id, line in enumerate(list_of_text_lines):
        code_character = ord(line[0].lower())

        if ord('а') <= code_character <= ord('я') or code_character == ord('ё'):
            letters = letters_ru
        elif ord('a') <= code_character <= ord('z'):
            letters = letters_en
        else:
            raise Exception('Unexpected letters. Probably this language is not supported.')

        encrypted_line = cesar_encryption(line, line_id + 1, letters)
        encrypted_list.append(encrypted_line)

    return encrypted_list


def encrypted_lines_show(list_of_text_lines, encrypted_list):
    print('\nThe result of encryption: ')
    for id, item in enumerate(list_of_text_lines):
        print(f'{id + 1}. {item} --> {encrypted_list[id]}')
    print()


def Caesars_cipher(directory):
    try:
        print('\nMake sure that one line in text file is written either in Russian or English letters.',
              'If you combine languages in one line, some letters will not be changed.',
              sep='\n')
        list_of_text_lines = file_reader(directory)
        encrypted_list = encryption_determination(list_of_text_lines)
        encrypted_lines_show(list_of_text_lines, encrypted_list)

    except Exception as error:
        print(error)
