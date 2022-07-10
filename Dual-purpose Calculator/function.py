import matplotlib.pyplot as plt
import numpy as np
from utils import calculate_equation, is_negative, OPERATORS_OPERATIONS
import sys

class Function():
    """Calculator's function mode"""

    def __init__(self):
        self.function_list = ['x']
        self.domain = [-10, 10]
        self.samples = 100

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        if value[0] >= value[1]:
            print('Left domain cannot be a higher value than ' +
                'a right domain!')
            sys.exit()
        self._domain = value

    @property
    def samples(self):
        return self._samples

    @samples.setter
    def samples(self, value):
        if value <= 0:
            print('Number of samples must be higher than 0!')
            sys.exit()
        self._samples = value

    @property
    def function_list(self):
        return self._function_list
    
    @function_list.setter
    def function_list(self, value):
        if len(value) <= 0:
            print('Equation must exist!')
            sys.exit()
        for char in value:
            if not char.isdigit() and not is_negative(char) and \
                char not in OPERATORS_OPERATIONS.keys() and \
                char not in ['x', '(', ')']:
                print('Equation can only contain sign "x" as an unknown in a ' +
                    'function.')
                sys.exit()
        self._function_list = value

    def substitute_variable(self, func, variable, value):
        """
        Substitutes given variable for value in a given string array function.

        Arguments:
        func - function to substitute value for a variable
        variable - variable (sign/character) that has to be substituted
        value - value that will be substituted for a variable

        Returns: array with substituted variables
        """
        func_copy = func.copy()

        for i, sign in enumerate(func_copy):
            if sign == variable:
                func_copy[i] = value

        return func_copy

    def draw_function(self):
        """
        Draws function (using matplotlip.pyplot) based on equation 
        in function_list.
        """
        t = np.linspace(self.domain[0], self.domain[1], self.samples)
        args = []

        for v in t:
            args.append(float(calculate_equation(
                self.substitute_variable(self.function_list, 'x', str(v)))))

        plt.plot(t, args)

        plt.axhline(y=0, color='grey')
        plt.axvline(color='grey')

        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        plt.title(f'Graph of {"".join(self.function_list)}')
        plt.xlabel('x')

        plt.show()

    def start(self):
        try:
            print('Write equation of the function that you want to draw:')
            func = input()

            domain = []
            domain.append(int(input('Left domain of a function: ')))
            domain.append(int(input('Right domain of a function: ')))
            self.domain = domain

            self.samples = int(input('Number of samples to calculate: '))

            self.function_list = [char for char in func if char != ' ']
            self.draw_function()
        except:
            print('An error has occured. Try again.')