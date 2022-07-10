from utils import float_string_to_int, calculate_equation

class Basic:
    """Calculator's basic mode"""

    def start(self):
        try:
            print('Write your equation to calculate:')
            equation = input()
            print(f'Result: {float_string_to_int(calculate_equation(equation))}')
        except:
            print('An error has occured. Try again.')