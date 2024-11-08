from src.classes import Soda, Math, Car, Sphere, SuperStr

class T1SodaFlavour:
    def __init__(self, correct_input):
        self._input_check = correct_input
        self._flavour = None

    def execute(self):
        while True:
            try:
                string= input('\nWhat is the taste of your soda? ')
                self._flavour = self._input_check.word_determination(string)
                break
            except Exception as exception:
                print(exception)

        soda = Soda(self._flavour)
        soda.soda_taste()


class T2Math:

    def __init__(self, correct_input):
        self._input_check = correct_input
        self._items = ['\n1. Addition', '2. Subtraction', '3. Multiplication', '4. Division', '5. Exit Math']

    def _input_determination(self, operation):
        dict_of_operations = {
            '+': ('first summand', 'second summand'),
            '-': ('reducible', 'subtraction'),
            '*': ('first multiplier', 'second multiplier'),
            '/': ('divisor', 'delimiter')
        }

        tuple_of_text = dict_of_operations[operation]
        while True:
            try:
                number_1 = input(f'\nWhat is the {tuple_of_text[0]}: ')
                number_2 = input(f'What is the {tuple_of_text[1]}: ')

                if operation == '/':
                    number_1, number_2 = self._input_check.math_number_division_check(number_1=number_1, number_2=number_2)
                else:
                    number_1, number_2 = self._input_check.math_number_check(number_1=number_1, number_2=number_2)
                break

            except Exception as exception:
                print(exception)
        return number_1, number_2


    def execute(self):
        calculator = Math()
        while True:
            list(map(lambda item: print(item), self._items))
            choice = None
            try:
                choice = input('\nChoose the Math point: ')
                choice = self._input_check.menu_point_validation(choice=choice, menu_length=len(self._items))
            except Exception as exception:
                print(exception)

            match choice:
                case 1:
                    number_1, number_2 = self._input_determination('+')

                    result = calculator.addition(num_1=number_1, num_2=number_2)

                case 2:
                    number_1, number_2 = self._input_determination('-')

                    result = calculator.subtraction(num_1=number_1, num_2=number_2)

                case 3:
                    number_1, number_2 = self._input_determination('*')

                    result = calculator.multiplication(num_1=number_1, num_2=number_2)

                case 4:
                    number_1, number_2 = self._input_determination('/')

                    result = calculator.division(num_1=number_1, num_2=number_2)

                case 5:
                    return False

                case None:
                    return False


class T3Car:
    def __init__(self, correct_input):
        self._input_check = correct_input
        self._items = ['\n1. Engage', '2. Muffle','3. Set Type', '4. Set Year',
                       '5. Set Color', '6. Car Info', '7. Exit Car']
        self._list_of_car_determination = ['What is the type of your car: ', 'What is the year of your car: ',
                                           'What is the color of your car: ']
        self._color = None
        self._year = None
        self._type = None

    def _car_determinations(self):
        self._type = self._input_check.input_check_branching(input_text=self._list_of_car_determination[0],
                                                             method=self._input_check.word_determination)
        self._year = self._input_check.input_check_branching(input_text=self._list_of_car_determination[1],
                                                             method=self._input_check.four_digit_number_determination)
        self._color = self._input_check.input_check_branching(input_text=self._list_of_car_determination[2],
                                                              method=self._input_check.word_determination)

        return Car(car_type=self._type, year=self._year, color=self._color)

    def execute(self):
        car = self._car_determinations()
        car.get_info()
        while True:
            list(map(lambda item: print(item), self._items))
            choice = None
            try:
                choice = input('\nChoose the Car point: ')
                choice = self._input_check.menu_point_validation(choice=choice, menu_length=len(self._items))
            except Exception as exception:
                print(exception)

            match choice:
                case 1:
                    car.engage()
                case 2:
                    car.muffle()
                case 3:
                    self._type = self._input_check.input_check_branching(input_text=self._list_of_car_determination[0],
                                                                         method=self._input_check.word_determination)
                    car.set_car_type(car_type=self._type)
                case 4:
                    self._year = self._input_check.input_check_branching(input_text=self._list_of_car_determination[1],
                                                             method=self._input_check.four_digit_number_determination)
                    car.set_year(year=self._year)
                case 5:
                    self._color = self._input_check.input_check_branching(input_text=self._list_of_car_determination[2],
                                                                  method=self._input_check.word_determination)
                    car.set_color(color=self._color)
                case 6:
                    car.get_info()
                case 7:
                    return False
                case None:
                    return False


class T4Sphere:
    def __init__(self, correct_input):
        self._list_of_sphere_determination = ['\nWhat is the radius of the sphere (cm): ', 'What is the x coord: ',
                                           'What is the y coord: ', 'What is the z coord: ']
        self._items = ['\n1. Ball volume', '2. External surface area of the ball', '3. Sphere radius',
                       '4. Sphere coords', '5. Set new radius', '6. Set new coords', '7. Is within the sphere',
                       '8. Sphere params', '9. Exit Sphere']
        self._input_check = correct_input
        self._is_set = True

    def _sphere_predetermination_phase(self):
        while True:
            try:
                string = input('\nDo you want to set any parameters for the sphere (yes/no) or (r/radius) for radius only?: ')
                choice = self._input_check.yes_or_no_determination(string=string)
                break
            except Exception as exception:
                print(exception)
        self._is_set = choice

    def coords_determination(self):
        x_coord = self._input_check.input_check_branching(input_text=self._list_of_sphere_determination[1],
                                                          method=self._input_check.sphere_coord_check)
        y_coord = self._input_check.input_check_branching(input_text=self._list_of_sphere_determination[2],
                                                          method=self._input_check.sphere_coord_check)
        z_coord = self._input_check.input_check_branching(input_text=self._list_of_sphere_determination[3],
                                                          method=self._input_check.sphere_coord_check)
        if not x_coord:
            x_coord = 0
        if not y_coord:
            y_coord = 0
        if not z_coord:
            z_coord = 0
        return x_coord, y_coord, z_coord

    def _sphere_determinations(self):
        self._sphere_predetermination_phase()

        if self._is_set is None:
            radius = self._input_check.input_check_branching(input_text=self._list_of_sphere_determination[0],
                                                             method=self._input_check.sphere_radius_check)
            if not radius:
                radius = 1

            return Sphere(radius=radius)

        elif self._is_set:
            radius = self._input_check.input_check_branching(input_text=self._list_of_sphere_determination[0],
                                                             method=self._input_check.sphere_radius_check)
            x_coord, y_coord, z_coord = self.coords_determination()

            if not radius:
                radius = 1
            return Sphere(radius=radius, x_coord=x_coord, y_coord=y_coord, z_coord=z_coord)

        else:
            return Sphere()


    def execute(self):
        sphere = self._sphere_determinations()
        sphere.show_info()
        while True:
            list(map(lambda item: print(item), self._items))
            choice = None
            try:
                choice = input('\nChoose the Sphere point: ')
                choice = self._input_check.menu_point_validation(choice=choice, menu_length=len(self._items))
            except Exception as exception:
                print(exception)

            match choice:
                case 1:
                    volume = sphere.ball_volume()
                    print(f'\n~ The volume of the sphere is: {volume} cm³.')

                case 2:
                    esa = sphere.get_square()
                    print(f'\n~ The square of external area of the sphere is: {esa} cm².')

                case 3:
                    radius = sphere.get_radius()
                    print(f'\n~ The radius of the sphere is: {radius} cm.')

                case 4:
                    coords = sphere.get_center()
                    print(f'\n~ The coords of the center of the sphere is: {coords} cm.')

                case 5:
                    radius = self._input_check.input_check_branching(input_text=self._list_of_sphere_determination[0],
                                                                     method=self._input_check.sphere_radius_check)
                    if not radius:
                        radius = 1
                    sphere.set_radius(radius=radius)

                case 6:
                    x_coord, y_coord, z_coord = self.coords_determination()
                    sphere.set_center(x_coord=x_coord, y_coord=y_coord, z_coord=z_coord)

                case 7:
                    print("\nLet's set the point coords: ")
                    x_coord, y_coord, z_coord = self.coords_determination()
                    is_in = sphere.is_point_inside(x_coord=x_coord, y_coord=y_coord, z_coord=z_coord)

                case 8:
                    sphere.show_info()

                case 9:
                    return False

                case None:
                    return False


class T5String:
    def __init__(self, correct_input):
        self._input_check = correct_input
        self._items = ['\n1. Set the string', '2. Repeatance check', '3. Palindrome check', '4. Exit String']

    def _first_string_determination(self, text = 'Enter the super string: '):
        try:
            string = input(f'\n{text}')
            return SuperStr(string)
        except:
            print('\n~ ### Warning. Something went wrong. Try again. ###')


    def execute(self):
        super_string = self._first_string_determination()

        while True:
            list(map(lambda item: print(item), self._items))
            choice = None
            try:
                choice = input('\nChoose the String point: ')
                choice = self._input_check.menu_point_validation(choice=choice, menu_length=len(self._items))
            except Exception as exception:
                print(exception)

            match choice:
                case 1:
                    super_string = self._first_string_determination()
                case 2:
                    target_super_string = self._first_string_determination(text='Enter the target string. The word case matters: ')
                    result = super_string.is_repetition(string=target_super_string)
                    if result:
                        print(f'\n~ "{super_string}" can be obtained by the number of integer repetitions of "{target_super_string}".')
                    else:
                        print(
                            f'\n~ "{super_string}" cannot be obtained by the number of integer repetitions of "{target_super_string}".')
                case 3:
                    result = super_string.is_palindrome()
                    if result:
                        print(f'\n~ "{super_string}" is a palindrome.')
                    else:
                        print(f'\n~ "{super_string}" is not a palindrome.')
                case 4:
                    return False
                case None:
                    return False


class Exit:
    def __init__(self):
        pass

    def execute(self):
        exit()
