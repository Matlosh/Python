# Functions used in more than one file

import re
import sys

def addition(a, b):
    return a + b

def subtraction(a, b):
    return a - b

def multiplication(a, b):
    return a * b

def division(a, b):
    if b != 0:
        return a / b
    else:
        print('Cannot divide by 0.')
        sys.exit()

def exponentiation(a, b):
    return a**b

OPERATORS_ORDER = {
    '+': 0,
    '-': 0,
    '*': 1,
    '/': 1,
    '^': 2
}

OPERATORS_OPERATIONS = {
    '+': addition,
    '-': subtraction,
    '*': multiplication,
    '/': division,
    '^': exponentiation
}

def is_float(item):
    """
    Check if given item is a float.
    
    Returns:
    True - if given item is a float
    False - if given item is not a float
    """
    if isinstance(item, float):
        return True

    if isinstance(item, int):
        return True

    if isinstance(item, str):
        item.strip()
        if re.fullmatch('^[0-9]+\.[0-9]+', item) or re.fullmatch('^-[0-9]+\.[0-9]+', item):
            return True
        else:
            return False

    return False

def is_negative(item):
    """
    Checks if given item (string) is a negative number (can be int or float).
    
    Returns:
    True - if given item is a negative number
    False - if given item is not a negative number
    """

    if isinstance(item, float):
        if item < 0:
            return True

    if isinstance(item, int):
        if item < 0:
            return True

    if isinstance(item, str):
        item.strip()
        if re.fullmatch('^-[0-9]+', item) or re.fullmatch('^-[0-9]+\.[0-9]+', item):
            return True
        else:
            return False

    return False

def join_numbers(arr):
    """
    Joins numbers in an given array.
    
    Returns: array with the joined numbers
    """
    arr_copy = arr.copy()

    i = 0
    try:
        while True:
            if arr_copy[i].isdigit() or is_negative(arr_copy[i]):
                if arr_copy[i + 1].isdigit():
                    arr_copy[i] = f'{arr_copy[i]}{arr_copy[i + 1]}'
                    del arr_copy[i+1]
                else:
                    i += 1
            elif arr_copy[i] == '.' and arr_copy[i + 1].isdigit():
                arr_copy[i - 1] = f'{arr_copy[i-1]}{arr_copy[i]}{arr_copy[i+1]}'
                del arr_copy[i:i+2]
                i -= 1
            elif is_float(arr_copy[i]):
                if arr_copy[i + 1].isdigit():
                    arr_copy[i] = f'{arr_copy[i]}{arr_copy[i+1]}'
                    del arr_copy[i+1]
                else:
                    i += 1
            elif arr_copy[i] == '-' and arr_copy[i+1].isdigit():
                if i == 0 or not arr_copy[i-1].isdigit() and \
                    not is_negative(arr_copy[i-1]) and \
                    not is_float(arr_copy[i-1]):
                    arr_copy[i] = f'{arr_copy[i]}{arr_copy[i+1]}'
                    del arr_copy[i+1]
                else:
                    i += 1
            else:
                i += 1
    except IndexError:
        return arr_copy

def join_factors(arr):
    """
    Joins factors with "x" in an given array.

    Returns: array with joined elements
    """
    arr_copy = arr.copy()
    arr_copy = join_numbers(arr_copy)

    i = 0
    try:
        while True:
            if arr_copy[i] == 'x':
                if arr_copy[i + 1] == '^' and arr_copy[i + 2].isdigit():
                    arr_copy[i] = f'{arr_copy[i]}{arr_copy[i+1]}{arr_copy[i+2]}'
                    del arr_copy[i+1:i+3]
                else:
                    i += 1
            else:
                i += 1
    except IndexError:
        return arr_copy

def last_index_of(arr, searched_element):
    """
    Find index of the last apperance of the element in an array.
    
    Returns: index of the last apperance of the element in an array
    """

    index = -1
    deleted = 0
    arr_copy = arr.copy()

    try:
        while True:
            index = arr_copy.index(searched_element)
            arr_copy.pop(index)
            deleted += 1
    except ValueError:
        return index + deleted  - 1

def float_string_to_int(number):
    """
    Converts float string to int only if possible.
    
    Returns: Converted float string to int
    """
    if isinstance(number, str):
        try:
            splitted = number.split('.')
            if splitted[1] == '0':
                return int(splitted[0])
        except IndexError:
            return number

    return number

def strip_of_numbers(arr):
    """
    Strips array of all numbers.
    
    Returns: array with stripped numbers
    """
    arr_copy = arr.copy()

    for i, char in enumerate(arr_copy):
        if char.isdigit() or is_negative(char) or float_string_to_int(char) \
            or float_string_to_int(char) == 0:
            del arr_copy[i]

    return arr_copy

def get_the_biggest_order(arr):
    """
    Gets the biggest order (order of operations) of given operands.
    
    Returns:
    int representing the biggest order of given operands
    if fails because of wrong operator, raises an exception
    """
    the_biggest_order = 0
    for i, operator in enumerate(arr):
        if operator in OPERATORS_ORDER.keys():
            if OPERATORS_ORDER[operator] > the_biggest_order:
                the_biggest_order = OPERATORS_ORDER[operator]
        elif operator == '.' and arr[i - 1].isdigit() and arr[i + 1].isdigit():
            pass
        else:
            raise Exception('Wrong operator')

    return the_biggest_order

def calculate_parenthesis(parenthesis_equation):
    """
    Calculate the equation inside one parenthesis.
    
    Returns: the calculated value in given parenthesis
    """
    equation = parenthesis_equation.copy()

    equation.pop(equation.index('('))
    equation.pop(equation.index(')'))

    equation = join_numbers(equation)
    operators = strip_of_numbers(equation)

    while len(operators) > 0:
        the_biggest_order = get_the_biggest_order(operators)
        for i, operator in enumerate(operators):
            if OPERATORS_ORDER[operator] == the_biggest_order:
                operator_index = equation.index(operator)
                left_operand = float(equation[operator_index - 1])
                right_operand = float(equation[operator_index + 1])

                result = str(round(OPERATORS_OPERATIONS[operator](left_operand, right_operand), 2))

                equation[(operator_index-1):(operator_index+2)] = result
                equation = join_numbers(equation)

                operators.pop(i)

    return equation[0]

def calculate_equation(equation):
    """
    Calculate equation (equation can contain parenthesis).
    
    Returns: the value of calculated equation
    """
    # Splitting string into an array by each character
    equation_list = [char for char in equation if char != ' ']

    # Adding '(' and ')' to secure calculation of the result
    equation_list.insert(0, '(')
    equation_list.append(')')

    is_counted = False

    if equation_list.count('(') == equation_list.count(')'):
        parenthesis_count = equation_list.count('(')

        while not is_counted:
            for _ in range(parenthesis_count):
                left_parenthesis = last_index_of(equation_list, '(')
                right_parenthesis = left_parenthesis + equation_list[left_parenthesis:].index(')') + 1

                parenthesis_equation = equation_list[left_parenthesis:right_parenthesis]
                parenthesis_result = calculate_parenthesis(parenthesis_equation)

                equation_list[left_parenthesis:right_parenthesis] = parenthesis_result

            is_counted = True

        return join_numbers(equation_list)[0]