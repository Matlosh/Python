from random import randint

class CPU:

    def __init__(self, dataset):
        self.dataset = dataset

    def make_move(self, field):
        """
        Makes move based on the provided field and dataset.
        
        Arguments:
        field - current game's field

        Returns:
        tuple - consisted of x and y position
        """

        def get_moves_count():
            """
            Counts number of moves made in the game.
            
            Arguments:
            field - current game's field
            
            Returns:
            number of moves made in the game
            """
            count = 0
            for row in field:
                for value in row:
                    if value != '.':
                        count += 1
            return count

        def compare_fields(dataset_field):
            """
            Compares current field with given dataset field.
            
            Arguments:
            dataset_field - field to compare with current game's
            field
                
            Returns:
            True - if fields are the same
            False - if fields aren't the same
            """
            for field_row, dataset_field_row in zip(field, dataset_field):
                if field_row != dataset_field_row:
                    return False
            return True

        def get_next_sign_position(dataset_field):
            """
            Finds next sign position with given dataset field
            (provided dataset_field should be almost exactly the same
            as current game's field - only one sign of difference).
            
            Arguments:
            dataset_field - field to compare with current game's
            field to find next sign position
            
            Returns:
            tuple (x, y) - next sign position
            '' - if fields are equal (this is only added to make my
            conscience clear)
            """

            for field_row, dataset_field_row, y \
                in zip(field, dataset_field, range(3)):
                if field_row != dataset_field_row:
                    for field_value, dataset_field_value, x in \
                        zip(field_row, dataset_field_row, range(3)):
                        if field_value != dataset_field_value:
                            return (x, y)
            return ''

        def is_field_value_empty(x, y):
            """
            Checks whether field's value position is empty (if field's value
            equals '.').
            
            Arguments:
            x - x position to check
            y - y position to check
            
            Returns:
            True - if field is empty
            False - if field isn't empty
            """

            if field[x][y] == '.':
                return True
            return False

        number_of_moves = get_moves_count()
        read_index = 1
        available_moves = []

        cpu_sign = 'x' if number_of_moves % 2 == 0 else 'o'

        for i in range(self.dataset.game_index):
            try:
                are_equal = compare_fields(self.dataset.read_game_state(
                    read_index, number_of_moves))
                winner_sign = self.dataset.read_game_winner(read_index)
                if are_equal and winner_sign == cpu_sign:
                    available_moves.append(self.dataset.read_game_state(
                        read_index, number_of_moves + 1))
                read_index += 1
            except:
                continue
        
        rand_move_pos = randint(0, len(available_moves)) - 1
        if rand_move_pos >= 0:
            return get_next_sign_position(available_moves[rand_move_pos])

        x, y = randint(0, 2), randint(0, 2)
        while field[y][x] != '.':
            x, y = randint(0, 2), randint(0, 2)
        return (x, y)