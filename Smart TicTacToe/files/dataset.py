import json

class Dataset:
    """Dataset for the TicTacToe games."""

    def __init__(self, file_path=''):
        """
        Arguments:
        file_path - path to a file with dataset which has to be opened
        (if file_path isn't given then the new dataset will be created)
        """
        self.dataset = {}
        self.game_index = 0

        if file_path:
            try:
                self.dataset, self.game_index = self.read_from_json_file(file_path)
            except:
                pass
    
    def create_new_game(self):
        """Creates new game in the dataset."""
        self.game_index = len(self.dataset) + 1
        self.dataset[self.game_index] = {}

    def insert_new_state(self, field):
        """
        Inserts new field state as next move in the dataset
        
        Arguments:
        field - field as list to fetch positions from
        """
        move_index = len(self.dataset[self.game_index]) + 1
        self.dataset[self.game_index][move_index] = {}
        sign_index = 1

        for y, row in enumerate(field):
            for x, sign in enumerate(row):
                if sign != '.':
                    self.dataset[self.game_index][move_index][sign_index] = {
                        'x': x,
                        'y': y,
                        'sign': sign
                    }
                    sign_index += 1

    def insert_game_result(self, sign):
        """
        Inserts game results.
        
        Arguments:
        sign - sign that won the game
        """
        self.dataset[self.game_index]['winner'] = sign

    def read_game_state(self, game_index, state_index):
        """
        Reads game state on given game and state index.
        
        Arguments:
        game_index - game index to read
        state_index - state index to read
        
        Returns:
        list containing field values"""
        game_state = self.dataset[str(game_index)][str(state_index)]
        field = [['.' for _ in range(3)] for _ in range(3)]

        for moves in game_state.values():
            field[moves["y"]][moves["x"]] = moves["sign"]

        return field

    def read_game_winner(self, game_index):
        """
        Reads game winner in given game index.
        
        Arguments:
        game_index - game index to read
        
        Returns:
        sign representing winner of the game"""

        return self.dataset[str(game_index)]["winner"]

    def convert_to_json(self):
        """
        Converts dataset to valid json format.
        
        Returns:
        dataset in json format
        """
        return json.dumps(self.dataset)

    def save_to_json_file(self, file_path):
        """Saves current dataset to a json file."""
        with open(file_path + '.json', 'w') as file:
            file.write(self.convert_to_json())

    def read_from_json_file(self, file_path):
        """Reads dataset from a json file.
        
        Returns:
        dictionary containing dataset
        number of recorded games in the dataset
        """
        with open(file_path + '.json', 'r') as file:
            dataset = json.load(file)
            return dataset, len(dataset)