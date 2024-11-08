##Функции шифрования и дешифрования
def string_input():
    while True:
        try:
            string = str(input('Введите строку из букв русского алфавита: '))
            break
        except:
            print("Что-то не так, попробуйте снова.")
            continue
    return(string)


def bias_input(letters):
    while True:
        try:
            bias = int(input('Введите смещение для шифра: '))
            break
        except:
            print('Смещение задано некорректно. Попробуйте еще раз.')
            continue
    bias = bias_check(bias, letters)
    return bias


def bias_check(bias, letters):
    while bias < 0:
        bias += len(letters)
    while bias > len(letters):
        bias -= len(letters)
    return bias

def isEncryption():
    print("1. Зашифровать",
          "2. Расшифровать",
          sep=';\n')
    while True:
        try:
            choice = int(input('Что требуется сделать со строкой: '))
        except:
            print('Вы ввели значение некорректно. Попробуйте еще раз')
            continue
        if choice <= 0 or choice > 2:
            continue
        return True if choice == 1 else False


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
            print(biased_position)
            new_char = additional_alphabet_dict[biased_position]
            if isUpper: new_char = new_char.upper()
            encrypted_string += new_char
        else:
            encrypted_string += char

    return encrypted_string


def cesar_decryption(string, bias, letters):
    main_alphabet_dict = {letter: index + 1 for index, letter in enumerate(letters)}
    additional_alphabet_dict = {index + 1: letter for index, letter in enumerate(letters)}
    letters_limit = len(letters)
    decrypted_string = ''
    for char in string:
        isUpper = True if char.isupper() else False
        if char.isalpha():
            char = char.lower()
            original_position = main_alphabet_dict[char]
            biased_position = original_position - bias

            if biased_position <= 0:
                overflow = letters_limit + biased_position
                biased_position = overflow
            else:
                pass
            new_char = additional_alphabet_dict[biased_position]
            if isUpper: new_char = new_char.upper()
            decrypted_string += new_char
        else:
            decrypted_string += char
    return decrypted_string


def cesar_determination(string, bias, isEncryption, letters):
    if isEncryption:
        print(f'\n### {string}',
              f'### {cesar_encryption(string, bias, letters)}',
              f'Смещение: {bias}.',
              sep=';\n'
        )
    else:
        print(f'\n### {string}',
              f'### {cesar_decryption(string, bias, letters)}',
              f'Смещение: {bias}.',
              sep=';\n'
              )


##Функции шифра виженера
def code_word_input():
    while True:
        try:
            code_word = str(input('Введите кодовое слово: '))
            single_code_word = ''.join(code_word.split())
            code_word = single_code_word.lower()
            break
        except:
            print('Вы ввели некорректное значение. Попробуйте еще раз')
            continue
    return code_word


def vigenere_determination(string, code_word, isEncryption, letters):
    if isEncryption:
        print(f'\n### {string}',
              f'### {vigenere_encryption(string, code_word, letters)}',
              f'Ключ: {code_word}.',
              sep=';\n')
    else:
        print(f'\n### {string}',
              f'### {vigenere_decryption(string, code_word, letters)}',
              f'Ключ: {code_word}.',
              sep=';\n')


def vigenere_encryption(string, code_word, letters):
    encrypted_text = ''
    code_word_current_position = 0
    main_alphabet_dict = {letter: index + 1 for index, letter in enumerate(letters)}
    for index, char in enumerate(string):
        if char.isalpha():

            if code_word_current_position > len(code_word) - 1:
                code_word_current_position = 0
            else:
                pass

            bias = main_alphabet_dict[code_word[code_word_current_position]]
            new_char = cesar_encryption(char, bias, letters)
            encrypted_text += new_char
            code_word_current_position += 1
        else:
            encrypted_text += char

    return encrypted_text


def vigenere_decryption(string, code_word, letters):
    decrypted_text = ''
    code_word_current_position = 0
    main_alphabet_dict = {letter: index + 1 for index, letter in enumerate(letters)}
    for index, char in enumerate(string):
        if char.isalpha():

            if code_word_current_position > len(code_word) - 1:
                code_word_current_position = 0
            else:
                pass

            bias = main_alphabet_dict[code_word[code_word_current_position]]
            new_char = cesar_decryption(char, bias, letters)
            decrypted_text += new_char
            code_word_current_position += 1
        else:
            decrypted_text += char

    return decrypted_text
