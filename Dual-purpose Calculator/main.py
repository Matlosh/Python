# Author: Matlosh, 2022
# https://github.com/Matlosh

import sys
import textwrap
from basic import Basic
from function import Function

def mode(argument):
    """Connected with '-m' argument."""

    def basic_mode():
        basic = Basic()
        basic.start()

    def function_mode():
        function = Function()
        function.start()

    modes = {
        'basic': basic_mode,
        'function': function_mode,
    }

    index = sys.argv.index(argument)

    if index + 1 < len(sys.argv) and sys.argv[index + 1] in modes.keys():
        modes[sys.argv[index + 1]]()
    else:
        print(f'Error: Pass the correct value to {argument} argument.')

def help(argument):
    """Connected with '-h' argument."""

    arguments = {
        'default': """
            Help:

            -h, --help -> shows help
                available arguments: [none, basic, function]
                example: -h function
            -m, --mode -> allows to choose calculator's mode:
                available modes: [basic, function]
                example: -m basic""",
        'basic': """
            Help for "basic" mode:

            In basic mode, user can write operation composed of any of the
            accepted signs. After submitting message with calculated result
            will be shown.

            Available signs and their mathematical meaning:
                + -> addition
                - -> subtraction
                / -> division
                * -> multiplication
                ^ -> exponentation (power)
                ( -> parenthesis opening
                ) -> parenthesis closing
                0-9 -> digits""",
        'function': """
            Help for "function" mode:

            In function mode, user can generate a function's illustration by 
            giving a function formula composed of any of the accepted signs and 
            with unknown "x" in it. (Note: only sign "x" is accepted!) Next, 
            user can state left and right domain of the function and number of
            samples to calculate function values. After submitting drawn function
            should be shown.

            Arguments given on the start of the program:
                function's formula -> function's formula to draw
                left domain -> left domain of the function
                right domain -> right domain of the function
                samples -> number of samples to create (the higher the number of 
                    samples the more time it will take to draw a function, but 
                    the function's illustration will be more precise)

            Available signs and their mathematical meaning:
                + -> addition
                - -> subtraction
                / -> division
                * -> multiplication
                ^ -> exponentation (power)
                ( -> parenthesis opening
                ) -> parenthesis closing
                0-9 -> digits
                x -> unknown variable"""
    }

    index = sys.argv.index(argument)
    help_info = ''

    if index + 1 < len(sys.argv) and sys.argv[index + 1] in arguments.keys():
        help_info = arguments[sys.argv[index + 1]]
    else:
        help_info = arguments['default']

    print(textwrap.dedent(help_info))

arguments = {
    '-m': mode,
    '--mode': mode,
    '-h': help,
    '--help': help
}

def main():
    if len(sys.argv) >= 2:
        for argument in sys.argv:
            if argument in arguments:
                arguments[argument](argument)
                break
    else:
        print('Mode has to be chosen in order to start the calculator!')

if __name__ == '__main__':
    main()