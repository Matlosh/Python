import sys
from dataset import Dataset
from cpu import CPU

class TicTacToe:

    def __init__(self, p1_name='Player', p2_name='CPU', p1_sign='x', p2_sign='o',
        p1_CPU=False, p2_CPU=True, dataset_path='', training_counter=0):
        self.field = []
        self.player1 = {'name': p1_name, 'sign': p1_sign, 'isCPU': p1_CPU}
        self.player2 = {'name': p2_name, 'sign': p2_sign, 'isCPU': p2_CPU}
        self.dataset_path = dataset_path

        if dataset_path == '':
            self.dataset = Dataset()
            self.dataset_path = 'dataset'
        else:
            self.dataset = Dataset(dataset_path)

        self.training_counter = training_counter
        self.is_playing = False

    def start(self):
        """Starts the new TicTacToe game."""
        self.is_playing = True
        while self.is_playing:
            self.game()

    def game(self):
        """Starts the new TicTacToe game."""
        has_ended = False
        current_player = self.player1
        self.field = [['.' for _ in range(3)] for _ in range(3)]
        self.dataset.create_new_game()

        cpu = CPU(self.dataset)

        def check_for_end():
            """
            Checks whether the game has ended and if user wants to end
            the game. Depending on user choice saves dataset to a file
            or starts the new game.
            
            Returns:
            True - if the game has ended
            False - if the game hasn't ended
            """

            def get_empty_space(field):
                """
                Counts empty space in the given field (all the values
                that equal to '.') and returns it.

                Arguments:
                field - field to count empty space from

                Returns:
                number of empty vields
                """
                empty = 0
                for row in field:
                    for value in row:
                        if value == '.':
                            empty += 1
                return empty

            if self.check_for_win(current_player['sign']) or \
                get_empty_space(self.field) == 0:
                nonlocal has_ended

                if self.check_for_win(current_player['sign']) or \
                    not get_empty_space(self.field) == 0:
                    print(f"{current_player['name']} won!")
                    self.dataset.insert_game_result(current_player['sign'])
                else:
                    print('Draw!')
                    self.dataset.insert_game_result('draw')

                self.show_field()

                if self.player1['isCPU'] and self.player2['isCPU'] and \
                    self.training_counter > 1:
                    should_end = False
                    self.training_counter -= 1
                elif self.player1['isCPU'] and self.player2['isCPU'] and \
                    self.training_counter <= 1:
                    should_end = True
                else:
                    should_end = self.check_for_end()
                has_ended = True

                if should_end:
                    self.dataset.save_to_json_file(self.dataset_path)
                    self.is_playing = False
                return True
            return False

        while not has_ended:
            if not current_player['isCPU']:
                x = input(f"'x' pos of {current_player['name']}'s sign: ")
                y = input(f"'y' pos of {current_player['name']}'s sign: ")

                while not self.insert_sign(x, y, current_player['sign']):
                    print("Wrong position was passed. Pass it once again.")
                    x = input(f"'x' pos of {current_player['name']}'s sign: ")
                    y = input(f"'y' pos of {current_player['name']}'s sign: ")

                if check_for_end():
                    break
            else:
                x, y = len(self.field[0]), len(self.field)

                while not self.insert_sign(x, y, current_player['sign']):
                    x, y = cpu.make_move(self.field)

                if check_for_end():
                    break

                print("\n")

            self.show_field()

            if current_player == self.player1:
                current_player = self.player2
            else:
                current_player = self.player1

    def insert_sign(self, x, y, sign):
        """
        Inserts given sign at given x and y position in the field.

        Arguments:
        x - point representing a column to insert
        y - point representing a row to insert
        sign - character which will be inserted to field

        Returns:
        True - if mark was successfully added
        False - if mark wasn't added
        """
        try:
            x = int(x)
            y = int(y)
        except:
            return False

        if x < len(self.field[0]) and y < len(self.field):
            if self.field[y][x] == '.':
                self.field[y][x] = sign
                self.dataset.insert_new_state(self.field)
                return True
        return False

    def check_for_win(self, sign):
        """
        Simply checks if field contains any of the win patterns.

        Arguments:
        sign - mark to check for win

        Returns:
        True - if field contains any of the winning patterns
        False - if field doesn't contain any of the winning patterns
        """

        def check_list(list):
            """
            Checks if any of the list rows contains all the same characters

            Arguments:
            list - list to go over and compare rows' elements
            """
            for row in list:
                iterator = iter(row)
                if all(x == sign for x in iterator):
                    return True
            return False

        # first pattern - the same signs in the row

        # second pattern - the same signs in the column
        columns = [[] for _ in self.field]
        for i, row in enumerate(self.field):
            for j, cell in enumerate(row):
                columns[j].append(cell)

        # third pattern - the same signs in the cross
        cross = [[], []]
        # checks if field is a square
        if len(self.field) == len(self.field[0]):
            for i in range(len(self.field)):
                field_length = len(self.field) - 1
                cross[0].append(self.field[i][i])
                cross[1].append(self.field[field_length - i][i])

        return check_list(self.field) or check_list(columns) or check_list(cross)

    def check_for_end(self):
        """
        Checks whether user wants to end playing the game.
        
        Returns:
        True - if user wants to end the game (responded with "yes")
        False - if user doesn't want to end the game 
        (responded with "no")
        """
        response = ''

        while response != 'yes' and response != 'no':
            response = input('Do you want to end playing? (yes/no): ')

        return True if response == 'yes' else False

    def show_field(self):
        """Prints current game field."""
        for row in self.field:
            rowString = ''
            for value in row:
                rowString += value
            print(rowString)

def usages():
    """Prints the help page and exits."""

    help_lines = (
        'Available commands:',
        ' -h, -help -> shows this page',
        ' -dp=, -dp= -> path to already existing dataset',
        '(path to dataset has to be written after "=" sign)',
        ' -t=, -train= -> enables training mode (enables to create and',
        'insert result data into the dataset from the randomly' ,
        'generated games)',
        '(number of results to insert into the dataset has to be',
        'written after the "=" sign)'
    )

    print('\n'.join(help_lines))
    exit()

def main():
    """
    Checks command for optional arguments and sets the adequate mode 
    and launches the game.
    """
    game_config = {'p1_name': 'Player', 'p2_name': 'CPU', 'p1_sign': 'x',
        'p2_sign': 'o', 'p1_CPU': False, 'p2_CPU': True, 'dataset_path': '',
        'training_counter': 0}

    for arg in sys.argv:
        # Training mode
        if any([x in arg for x in ['-train=', '-t=']]):
            game_config['p1_name'] = 'CPU1'
            game_config['p2_name'] = 'CPU2'
            game_config['p1_CPU'] = True
            game_config['training_counter'] = int(arg.split('=')[1])
            continue

        if any([x in arg for x in ['-dataset_path=', '-dp=']]):
            game_config['dataset_path'] = arg.split('=')[1]
            continue

        if any([x in arg for x in ['-h', '-help']]):
            usages()
    
    game = TicTacToe(**game_config)
    game.start()

if __name__ == '__main__':
   main()