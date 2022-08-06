import json, random, textwrap, os

class GuessTheCountry:

    def __init__(self):
        # Default settings
        self.settings = {
            'with_additional_info': True,
            'region_to_guess': 'World',
            'lives_per_game': 3,
            'countries_data_path': 'countries_data.json',
            'statistics_save_path': 'statistics.json',
            'settings_save_path': 'settings.json'
        }

        self.load_settings()
        self.load_countries_data()

    def load_countries_data(self):
        with open(self.settings['countries_data_path']) as data:
            self.countries_data = json.loads(data.read())

    def load_settings(self):
        self.settings = \
            self.read_json_from_file(self.settings['settings_save_path'],
            self.settings)

    def load_statistics(self):
        self.statistics = self.read_json_from_file(
            self.settings['statistics_save_path'], {})

    def save_json_to_file(self, file_path: str , obj_to_dump: object, 
        indent: int=None):
        """Saves given Python's object to the given file with optional
        indent (can make saved file "pretty")."""
        if os.path.dirname(file_path) != '' and \
            not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        with open(file_path, 'w') as file:
            json.dump(obj_to_dump, file, indent=indent)

    def read_json_from_file(self, file_path, default=None):
        """Reads a json from the file and returns it."""
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        return default

    def show_statistics(self):
        """Shows the game statistics."""
        self.load_statistics()

        table_header_values = [
            'Country name', 'Correctly guessed', 'Wrongly guessed'
        ]
        table_header_row = ''

        for i, value in enumerate(table_header_values):
            if i > 0:
                table_header_row += f' | {value}'
            else:
                table_header_row += value

        table_rows = []
        for country_name, country_statistics in self.statistics.items():
            country_entry = f'{country_name}'
            for statistics in country_statistics.values():
                country_entry += f' | {statistics}'

            table_rows.append(country_entry)

        print(table_header_row)
        if len(table_rows) > 0:
            longest_values_len = [0 for _ in table_rows[0].split('|')]
            table_row_values_split = []
            for table_row in table_rows:
                values = table_row.split('|')
                values = [value.strip() for value in values]

                for i, value in enumerate(values):
                    if len(value) > longest_values_len[i]:
                        longest_values_len[i] = len(value)

                table_row_values_split.append(values)

            formatted_table_rows = []
            for values in table_row_values_split:
                formatted_table_row = ''
                for i, value in enumerate(values):
                    formatted_table_row += value + (' ' * \
                        (longest_values_len[i] - len(value))) + '|'

                formatted_table_rows.append(formatted_table_row)

            for formatted_table_row in formatted_table_rows:
                print(formatted_table_row)

    def get_all_available_options(self, countries_data, option_name,
        *default_options):
        """Searches countries data for all options and returns 
        a set of them.
        Note: default_options arg adds the given options regardless
        the found ones"""
        options = set()

        for country_data in countries_data:
            options.add(country_data[option_name])

        for default_option in default_options:
            options.add(default_option)

        return options

    def show_settings(self):
        """Shows available settings and allows to change them."""
        def change_bool(option_key: str):
            while True:
                new_value = \
                    input(f'{option_key}: change to [True/False] ').lower()
                if new_value in ['true', 'false']:
                    return bool(1) if new_value == 'true' else bool(0)

        def change_str(option_key: str, suggested_values: set={}):
            suggested_values_text = ''
            if len(suggested_values) == 0:
                suggested_values_text = ["Any values"]
            else:
                suggested_values_text = '['
                for suggested_value in suggested_values:
                    suggested_values_text += f'{suggested_value}/'
                suggested_values_text = suggested_values_text[:-1]
                suggested_values_text += ']'

            suggested_values_lower = {val.lower(): val for val in suggested_values}

            while True:
                new_value = \
                    input(f'{option_key}: change to {suggested_values_text} ')
                if len(suggested_values) > 0:
                    if new_value.lower() in suggested_values_lower.keys():
                        return suggested_values_lower[new_value.lower()]
                else:
                    return new_value

        def change_int(option_key: str, minimal_value=None):
            minimal_value_text = ["Any number"]
            if isinstance(minimal_value, int):
                minimal_value_text = f'[Minimal value: {minimal_value}]'
            
            while True:
                new_value = \
                    input(f'{option_key}: change to {minimal_value_text} ')

                if new_value.isnumeric():
                    if int(new_value) >= minimal_value:
                        return int(new_value)
                    else:
                        continue
                else:
                    continue

        option_change_pattern = {
            bool: change_bool,
            str: change_str,
            int: change_int
        }

        additional_arguments = {
            'region_to_guess': \
                self.get_all_available_options(self.countries_data, 'region',
                    'World'),
            'lives_per_game': 1
        }

        reload_data = {
            'countries_data_path': lambda: self.load_countries_data(),
            'statistics_save_path': lambda: self.load_statistics()
        }

        while True:
            print('0. Return')
            for i, (option_key, option_value) in enumerate(self.settings.items()):
                option = f'{i+1}. {option_key}: {option_value}'
                print(option)
            to_change = int(input('\nWhich option do you want to change? '))

            if to_change == 0:
                self.save_json_to_file(self.settings['settings_save_path'], 
                    self.settings, indent=4)
                break

            try:
                option_key, option_value = \
                    list(self.settings.items())[to_change-1]

                if type(option_value) == bool:
                    self.settings[option_key] = \
                        option_change_pattern[type(option_value)](option_key)
                else:
                    self.settings[option_key] = \
                        option_change_pattern[type(option_value)](option_key,
                            additional_arguments.get(option_key, {}))
                    # check below and updating reloaded paths
                    reload_data.get(option_key, None)
                print(' ')
            except:
                break

    def update_statistics_entry(self, country_name: str, did_win: bool):
        """Adds new entry to the statistics list if it doesn't exist or
        updates if it does."""
        if country_name not in self.statistics.keys():
            self.statistics[country_name] = {
                'correctly_guessed': 0,
                'wrongly_guessed': 0
            }

            # Sorting dict alphabetically
            sorted_keys = sorted(self.statistics.keys())
            sorted_statistics = {}

            for keys in sorted_keys:
                sorted_statistics[keys] = self.statistics[keys]
            
            self.statistics = sorted_statistics

        if did_win:
            self.statistics[country_name]['correctly_guessed'] = \
                self.statistics[country_name]['correctly_guessed'] + 1
        else:
            self.statistics[country_name]['wrongly_guessed'] = \
                self.statistics[country_name]['wrongly_guessed'] + 1

    def insert_letter(self, letter: str, answer: list, user_answer: list):
        """Checks whether the given letter is in the answer, if is then 
        returns corrected user answer, else returned user answer stays the 
        same as it was passed in the argument."""
        user_answer_copy = user_answer.copy()
        for i, answer_letter in enumerate(answer):
            if letter.lower() == answer_letter.lower():
                user_answer_copy[i] = answer_letter

        return user_answer_copy

    def print_user_answer(self, user_answer):
        """Returns the user answer (as str)."""
        print_str = ''
        for letter in user_answer:
            print_str += letter
        return print_str

    def menu(self):
        """Game's menu."""
        menu = """
        1. Guess The Country
        2. Statistics
        3. Settings
        4. Exit
        """

        menu_options = {
            1: self.start_game,
            2: self.show_statistics,
            3: self.show_settings,
            4: exit
        }

        while True:
            choice = 0
            while True:
                print(textwrap.dedent(menu))
                choice = int(input("What's your choice? "))
                
                if choice in menu_options.keys():
                    print('')
                    break
            
            menu_options[choice]()

    def start_game(self):
        """Game's main loop."""

        self.load_statistics()

        while True:
            self.guess_the_country()

            question = input('Do you want to play again? (y/n) ').lower()
            if question == 'y':
                continue
            else:
                self.save_json_to_file(self.settings['statistics_save_path'], self.statistics)
                break

    def guess_the_country(self):
        """Guess the country game."""

        country_id = 0

        while True:
            country_id = random.randint(0, len(self.countries_data) - 1)

            if self.settings['region_to_guess'] == 'World':
                break

            if self.countries_data[country_id]['region'] == \
                self.settings['region_to_guess']:
                break

        answer = self.countries_data[country_id]['name']['common']
        country_data = self.countries_data[country_id]

        additional_info = f"""
        Capital: {country_data['capital']}
        Area: {country_data['area']}
        Borders: {country_data['borders']}
        Region: {country_data['region']}
        Subregion: {country_data['subregion']}
        """

        lives = self.settings['lives_per_game']
        user_answer = ['_' if letter != ' ' else ' ' 
            for letter in answer]
        did_win = False
        used_letters = []

        print(self.print_user_answer(user_answer))
        
        if self.settings['with_additional_info']:
            print(textwrap.dedent(additional_info))

        while lives != 0:
            user_input = input('Letter or the answer: ')

            if len(user_input) == 1:
                if user_input not in used_letters:
                    user_answer_with_inserted = self.insert_letter(user_input, 
                        answer, user_answer)
                    if user_answer_with_inserted != user_answer:
                        user_answer = user_answer_with_inserted
                    else:
                        lives -= 1
                        print(f"This letter doesn't occur in the name of the " +
                            f"country, remaining lives: {lives}")
                    used_letters.append(user_input)
                else:
                    print('This letter was already used!')
            elif len(user_input) > 1:
                if user_input == answer:
                    did_win = True
                    break
                else:
                    lives -= 1
                    print(f'Wrong answer, remaining lives: {lives}')
            else:
                print(f'Letter or answer has to be written!')
                continue

            print(self.print_user_answer(user_answer))

            if user_answer.count('_') == 0:
                did_win = True
                break

        if did_win:
            print('You correctly guessed the country, congratulations!')
        else:
            print(f'You did not guess the country, the answer was: {answer}')

        self.update_statistics_entry(answer, did_win)

if __name__ == '__main__':
    guess_the_country = GuessTheCountry()
    guess_the_country.menu()