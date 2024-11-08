import math
from math import pow, sqrt, cos, sin

def formula_working ():
    """
    Функция узнает у пользователя значения до тех пор, пока не будут введены значения требуемого типа.
    Значения подставляются в формулы.
    """
    print("Для расчета формул требуется ввести некоторые значения.")
    acceptance_flag = False
    while not acceptance_flag:
        try:
            a = int(input('Введите значение переменной a: '))
            b = int(input('Введите значение переменной b: '))
            if b == 0 :
                print('Для решения данной задачи b не может быть равно 0. Начните сначала.')
            x = int(input('Введите значение переменной x: '))
            acceptance_flag = True
        except:
            print('Вы неверно вводите значение переменных')

    y1 = (pow(a,2) / 3) + ((pow(a, 2) + 4) / b) + (sqrt(pow(a, 2) + 4) / 4) + (sqrt(pow((pow(a, 2) + 4), 3)) / 4)
    y2 = cos(x) + sin(x)
    y3 = pow(pow(cos(pow(x, 2)), 2) + pow(sin(2 * x - 1), 2), 1/3)
    y4 = 5 * x + 3 * pow(x, 2) * sqrt(1 + pow(sin(x), 2))

    print(f'\n{"-" * 40}',
          f'Для значений a = {a}, b = {b} и x = {x} результаты вычислений будут следующими: \n', sep='\n')

    print(f'1. {a}²/3 + ({a}²+4)/b + √({a}²+4)/4 + √({a}²+4)³/4 = {round(y1, 5)}',
          f'2. cos({x}) + sin({x}) = {round(y2, 5)}',
          f'3. ∛((cos²(x²) + sin²(2x - 1)) = {round(y3, 5)}',
          f'4. 5x + 3x² * √(1 + sin²(x)) = {round(y4, 5)}', sep=';\n')


def credits_calculator ():
    """
    Функция проверяет содержит в себе небольшой диалог, зависящий от введенных значений пользователем. Диалог содержит
    в себе проверки на допустимые значения в том числе. Проценты преобразуются в доли и вычисляется месячная процентная
    ставка путем деления доли на 12. Высчитывается полная сумма требуемая к выплате и переплата.
    """
    acceptance_flag = False
    print('Давайте посчитаем размер ежемесячной выплаты для Вашего кредита!')
    while not acceptance_flag:
        try:
            year_percentage = float(input('Введите годовую процентную ставку: '))
            print(percentage_checker(year_percentage))

            loan_amount = int(input('Укажите сумму займа в рублях: '))
            print(sum_checker(loan_amount))

            month_amount = int(input('И последнее.. И на сколько же месяцев Вы взяли кредит: '))
            print(month_checker(month_amount))

            if year_percentage <= 0 or loan_amount <= 0 or month_amount <= 0: continue

            acceptance_flag = True
        except:
            print('Что-то пошло не так, попробуйте ввести данные еще раз. Будьте внимательнее!')

        year_percentage /= 100
        per_month_payment = round(year_percentage / month_amount, 4)
        print(per_month_payment)
        print(loan_amount * per_month_payment * pow((1 + per_month_payment), month_amount))
        print(pow(1 + per_month_payment, month_amount) - 1)
        monthly_payment = (loan_amount * per_month_payment * pow((1 + per_month_payment), month_amount)) / \
            (pow(1 + per_month_payment, month_amount) - 1)
        overall_payment = round(monthly_payment * 12, 2)
        overprice = round(overall_payment - loan_amount, 2)


        print(f'\nСумма кредита - {loan_amount} рублей;',
              f'Процентная ставка - {year_percentage * 100}% в год;',
              f'Длительностью кредита - {month_amount} месяцев.',
              f'При таких условиях ежемесячный платеж составит {round(monthly_payment,2)} рублей.',
              f'Кроме того Вы переплатите {overprice} рублей, а общая сумма кредита - {overall_payment} рублей.',
              sep='\n')

def percentage_checker(percentage):
    dict_of_answers = {'liar':'- Меньше 0%? Вы врете.',
                       'great':'- Отлично, Вам крупно повезло урвать такой низкий процент!',
                       'good': '- Стандартная процентная ставка, все будет хорошо!',
                       'bad': '- Годовая процентная ставка большевата. Может стоит поискать другого кредитора?',
                       'even_worse' : '- Микрозаймы, да?(',
                       'special' : f'- {percentage}% ставка... Отличный выбор, грамотно подошли к кредитору.',
                       'hundred' : f'- {percentage}% в год сверху. А зачем Вам вообще что-то считать?',
                       'big_liar' : f'- Проверяешь возможности калькулятора? Ладно, посчитаю. '}
    if percentage <= 0:
        line = dict_of_answers['liar']
    elif percentage < 4:
        line = dict_of_answers['great']
    elif percentage < 8:
        line = dict_of_answers['good']
    elif percentage < 15:
        line = dict_of_answers['bad']
    elif percentage < 35:
        line = dict_of_answers['even_worse']
    elif percentage < 100:
        line = dict_of_answers['special']
    elif percentage == 100:
        line = dict_of_answers['hundred']
    else:
        line = dict_of_answers['big_liar']

    return line


def sum_checker (sum):
    dict_of_answers = {
        'liar' : '- Получается по нулям, да? Не пойдет. Еще разочек',
        'small' : '- Для кредита маловато, но имеем, что имеем',
        'medium' : '- Хорошенький такой займик, сейчас все посчитаем',
        'big' : '- Приятно иметь дело с серьезными людьми',
        'enormous' : '- Я боюсь даже представить, на что Вы его брали...'
    }

    if sum <= 0:
        line = dict_of_answers['liar']
    elif sum < 1000:
        line = dict_of_answers['small']
    elif sum < 10000:
        line = dict_of_answers['medium']
    elif sum < 100000:
        line = dict_of_answers['big']
    else:
        line = dict_of_answers['enormous']

    return line


def month_checker(amount_of_month):
    dict_of_answers = {
        'liar': '- По сути ведь это уже и не кредит вовсе.',
        '2-4': '- Чем меньше кредит, тем больше платишь.',
        'under_and_6': '- Время пролетит быстро, сейчас все посчитаем.',
        'under_and_12': '- Отлично, за год раскидаем долги. Сейчас посчитаю сколько именно платить надо будет.',
        'under_and_36': '- Срок приличный, но и платить в месяц меньше. Уже начал считать.',
        'under_and_120': '- Ого, кредит более трех лет. Должно быть сумма большая.',
        'under_and_480': '- Ипотека? Это мы сейчас быстро посчитаем.',
        'under_and_960': '- Это что за кредит? Жизненный...',
        'more_than_960': '- По наследству передать планируете? Уважаю.'
    }

    if amount_of_month <= 1:
        line = dict_of_answers['liar']
    elif amount_of_month <= 4:
        line = dict_of_answers['2-4']
    elif amount_of_month <= 6:
        line = dict_of_answers['under_and_6']
    elif amount_of_month <= 12:
        line = dict_of_answers['under_and_12']
    elif amount_of_month <= 36:
        line = dict_of_answers['under_and_36']
    elif amount_of_month <= 120:
        line = dict_of_answers['under_and_120']
    elif amount_of_month <= 480:
        line = dict_of_answers['under_and_480']
    elif amount_of_month <= 960:
        line = dict_of_answers['under_and_960']
    else:
        line = dict_of_answers['more_than_960']

    return line


def interstellar ():
    """
    Функция вычисляет длительность года в днях на планетах, значения радиуса орбит и орбитальных скоростей которых
    вводит сам пользователь. Поскольку по условию задачи радиус орбиты задается в млн. км., а скорость в км/ч, требуется
    произвести приведение к одним единицам. В данном случае радиус умножить на 10 в 6 степени, чтобы получить км. После
    чего можно подставлять в формулу. В результате получаем количество часов, которое делится на 24, чтобы получить сутки.
    Изначально производится проверка на ввод одинаковых данных, тогда вычисления производятся единожды. В противном случае
    После двух вычислений происходит сравнение и вывод нужной строки результата. Для проверки можно ввести значения Земли:
    R = 149.6 млн. км., а v = 107000 км/ч.
    """

    acceptance_flag = False
    while not acceptance_flag:
        try:
            radius_of_first_planet = float(input('Укажите радиус орбиты первой планеты в млн. км.: '))
            speed_of_first_planet = float(input('Отлично, подскажите орбитальную скорость планеты в км/ч: '))
            print(f'- Один миг, мне нужно проверить {radius_of_first_planet} и {speed_of_first_planet}. '
                  f'Мало ли что Вы мне написали.')
            if radius_of_first_planet <= 0 or speed_of_first_planet <= 0:
                print('- Так и думал... \n')
                continue
            else: print('- Все чудно, идем дальше. \n')

            radius_of_second_planet = float(input('Теперь радиус орбиты второй планеты: '))
            speed_of_second_planet = float(input('И последнее - ее орбитальная скорость: '))
            print('- Так, погоди-ка... Что-то здесь не так.')
            if radius_of_second_planet <= 0 or speed_of_second_planet <= 0:
                print('- Так и думал... Этого не может быть. \n')
                continue
            else:
                print('- Ну, вроде все нормально. \n')
            acceptance_flag = True


        except:
            print('- Я не понимаю, что это за цифры странные. Попробуйте еще разок. \n')
            continue

    if radius_of_second_planet == radius_of_first_planet and speed_of_first_planet == speed_of_second_planet:
        L = (2 * radius_of_first_planet * 10 ** 6 * math.pi) / speed_of_first_planet / 24
        print(f'Радиусы орбит обеих планет равны и орбитальные скорости одинаковы - Вы ввели данные одной планеты. Длина года'
              f' на ней - {round(L, 2)} дней.')
    else:
        L1 = (2 * radius_of_first_planet * 10 ** 6 * math.pi) / speed_of_first_planet / 24
        L2 = (2 * radius_of_second_planet * 10 ** 6 * math.pi) / speed_of_second_planet / 24
        print(f'\nДлина года на первой планете составляет {round(L1, 2)} дней, а на второй - {round(L2, 2)}.',
              f'Длина года на первой планете на {round(L1 - L2, 2)} дней больше чем на второй' if L1 > L2
              else f'Длина года на второй планете на {round(L2 - L1, 2)} дней больше чем на первой.',
              sep='\n')


def print_menu ():
    print(
        '\n',
        '1. Расчет четырех формул;',
        '2. Играл с кредитами - проиграл;',
        '3. Интерстеллар;',
        '4. Завершить работу.\n',
        sep='\n'
    )


if __name__ == "__main__":
    stop_flag = False
    while not stop_flag:
        print_menu()
        number_of_choice = int(input('Выберите номер: '))
        if number_of_choice <= 0 or number_of_choice > 4: continue
        match number_of_choice:
            case 1:
                formula_working()
            case 2:
                credits_calculator()
            case 3:
                interstellar()
            case 4:
                stop_flag = True