# Author: Matlosh, 2022
# https://github.com/Matlosh

import sys
from pydub import AudioSegment
import datetime
import os
from utils import ArgumentError, FolderNotFoundError, MusicManagerHelp
from playsound import playsound, PlaysoundException
import shutil
from pydub.playback import play

SUPPORTED_MUSIC_TYPES = ['mp3', 'wav', 'ogg']

# If anybody was worried how do I use words command/argument/value alternately
# here is a short explanation: command > arguments > values

class MusicManager:

    def __init__(self, argv):
        self.argv = argv

    def get_files_paths(self, values):
        """
        Gets available file paths from given values.
        
        Returns: Extracted file paths or empty list if none were found
        """
        files_paths = []

        for value in values:
            if value.split('.')[-1:][0] in SUPPORTED_MUSIC_TYPES:
                files_paths.append(value)

        return files_paths 

    def get_values(self, command, to_extract=0):
        """
        Gets values of a given command.
        
        Arguments:
        command - used command/argument
        to_extract - number of values to extract:
            (0 - extract till the end)

        Returns: Extracted values or empty list if none were found
        """
        command_index = self.argv.index(command)
        values = []

        if len(self.argv) - 1 > command_index:
            for i, value in enumerate(self.argv[command_index+1:]):
                if to_extract > 0 and i >= to_extract:
                    break
                values.append(value)
        else:
            return []

        return values

    def check_values(self, values, *banned_words):
        """
        Checks whether values don't contain any of the banned words.
        
        Returns:
        First found value that contains any of the banned words\n
        If any value doesn't contain any of the banned words returns
        empty string ('')
        """
        if len(values) > 0:
            for value in values:
                if value in banned_words:
                    return value
        
        return ''

    def separate_arguments(self, arguments_and_values, separators):
        """
        Separates command's arguments with their values.
        
        Returns:
        All arguments and their values in an array (each argument and their
        values is in separate array).
        """
        separated = []
        arg_a_val = arguments_and_values
        last_separator = arg_a_val[0]
        while True:
            arg_a_val = arg_a_val[1:]
            separator = self.check_values(arg_a_val, *separators)

            if separator and last_separator != separator:
                arg_a_val.insert(0, last_separator)

                separator_index = arg_a_val.index(separator)
                separated.append(arg_a_val[:separator_index])
                arg_a_val = arg_a_val[separator_index:]

                last_separator = separator
            else:
                arg_a_val.insert(0, last_separator)
                separated.append(arg_a_val)
                break

        return separated

    def execute_arguments(self, command, arguments_list, default_argument):
        """
        Executes all arguments of the given command, if any of the 
        arguments' aliases isn't provided, exectues the default one.
        """
        command_argv = self.argv[self.argv.index(command)+1:]
        args_n_val = self.separate_arguments(command_argv, 
            arguments_list.keys())

        if args_n_val[0][0] in arguments_list.keys():
            for arg_n_val in args_n_val:
                argument = arg_n_val[0]
                values = arg_n_val[1:]
                arguments_list[argument](argument, *values)
        else:
            arguments_list[default_argument](command, *args_n_val[0])

    def check_values_length(self, function_name, expected_values_len, *values):
        """
        Simply checks arguments' values length.
        Method is mainly made just to prevent from making the same ifs and 
        elses in most of the methods.

        Throws error if length of the provided values is not equal to the
        expected length.
        """
        if len(values) != expected_values_len:
            raise ArgumentError(function_name, len(values),
                expected_values_len)

    def format_directory_path(self, path):
        """
        Checks if the given path to the directory contains '/' at the end.
        
        Returns: path with '/' at the end (if it didn't have it before)
        """
        path_copy = path
        if path_copy[-1:][0] != '/':
            path_copy += '/'
        return path_copy

    def join(self, command):
        """Joins all audio files."""

        # Settings
        save_path = 'created/'
        save_file_name = datetime.datetime.now().strftime('%H_%M_%S_%Y_%m_%d')
        save_file_type = 'mp3'
        save_file_bitrate = '192k'
        gap_duration = 0
        crossfade_duration = 0

        def files(argument, *values):
            """
            Joins files with given paths to files. 
            (Files must be of accepted file types in order to join)
            """
            files_paths = self.get_files_paths(values)

            joined_sounds = AudioSegment.empty()
            for i, file_path in enumerate(files_paths):
                audio_to_join = AudioSegment.from_file(file_path, 
                    format=file_path.split('.')[-1:][0])

                if i > 0:
                    joined_sounds = joined_sounds.append(audio_to_join,
                        crossfade=crossfade_duration)
                else:
                    joined_sounds += audio_to_join
                joined_sounds += AudioSegment.silent(
                    duration=gap_duration)

            joined_sounds.export(f'{save_path}{save_file_name}.mp3',
                format=save_file_type, bitrate=save_file_bitrate)

        def save(argument, *values):
            """
            Changes save path from the default one.
            
            Raises an error if any value wasn't provided.
            """            
            # check below
            # and -p -r -f
            self.check_values_length(save.__name__, 1, *values)

            nonlocal save_path
            save_path = self.format_directory_path(values[0])
            if not os.path.isdir(save_path):
                os.mkdir(save_path)

        def name(argument, *values):
            """
            Changes file name from the default one.
            
            Raises an error if any value wasn't provided.
            """
            self.check_values_length(name.__name__, 1, *values)
            nonlocal save_file_name
            save_file_name = values[0]

        def folder(argument, *values):
            """
            Joins all files from given path to a folder.
            (Files must be of accepted file types in order to join)

            Raises an error if provided path to folder wasn't found.
            """
            self.check_values_length(folder.__name__, 1, *values)

            folder_path = values[0]
            if os.path.isdir(folder_path):
                files_paths = self.get_files_paths(os.listdir(folder_path))
                files_paths = [f'{folder_path}/{path}' for path in files_paths]
                files(*files_paths)
            else:
                raise FolderNotFoundError('Provided path to the folder is wrong.')

        def gap(argument, *values):
            """
            Changes default gap duration between each joined audio.
            Note: passed duration is in milliseconds.
            
            Raises an error if duration in wrong format was provided.
            """
            self.check_values_length(gap.__name__, 1, *values)
            
            nonlocal gap_duration
            gap_duration = values[0]
            if gap_duration.isdigit():
                gap_duration = int(gap_duration)
            else:
                raise ValueError('Unsupported format of gap ' +
                    'duration was provided.')

        def result_file_type(argument, *values):
            """
            Changes file type of the saved file from the default one.
            
            Raises an error if not supported file type is provided.
            """
            self.check_values_length(result_file_type.__name__, 1, *values)
            
            nonlocal save_file_type
            file_type = values[0]
            if values[0] in SUPPORTED_MUSIC_TYPES:
                save_file_type = file_type
            else:
                raise ValueError('Unsupported type for result' +
                    'file was provided.')

        def bitrate(argument, *values):
            """
            Changes bitrate of the result file from the default one.

            Raises an error if wrong format of bitrate is provided.
            """
            self.check_values_length(bitrate.__name__, 1, *values)

            nonlocal save_file_bitrate
            audio_bitrate = values[0]
            if audio_bitrate.isdigit() or audio_bitrate[:-1].isdigit() \
                and audio_bitrate[-1] == 'k':
                save_file_bitrate = values[0]
            else:
                raise ValueError('Wrong format of bitrate was provided.')

        def crossfade(argument, *values):
            """
            Changes default settings of crossfade.
            Note: passed duration is in milliseconds

            Raises an error if wrong format of duration was provided.
            """
            self.check_values_length(crossfade.__name__, 1, *values)

            nonlocal crossfade_duration
            duration = values[0]
            if duration.isdigit():
                crossfade_duration = int(duration)
            else:
                raise ValueError('Wrong format of duration was provided.')

        arguments_list = {
            '-fs': files,
            '-s': save,
            '-n': name,
            '-f': folder,
            '-g': gap,
            '-rft': result_file_type,
            '-b': bitrate,
            '-cr': crossfade
        }

        self.execute_arguments(command, arguments_list, '-fs')

    def play(self, command):
        """Plays an audio."""

        # Settings
        randomize_play = False

        def files(argument, *values):
            """
            Plays audios from given paths. 
            Note: If more than one path was passed, the audios will be 
                played in order (if it was not changed by other methods).
            """

            def remove_temp(file_path):
                if os.path.isfile(file_path):
                    os.remove(file_path)

            audio_paths = self.get_files_paths(values)

            if randomize_play:
                audio_paths = set(audio_paths)

            # audio = AudioSegment.empty()
            # audio += AudioSegment.from_file(audio_paths[0])[:5000]
            # audio.export('5secaudio.mp3', format='mp3')

            # playsound(...) can be just in the for loop, because
            # program work is actually paused for the time music
            # is playing
            for i, audio_path in enumerate(audio_paths):
                # deleting _temp.wav doesn't work when
                # KeyboardInterrupt raises
                try:
                    playsound(audio_path)
                except PlaysoundException:
                    # here is an error with permissions again...
                    # repair somehow, or do two files _temp1 and _temp2
                    # and remove _temp1 when _temp2 is used and vice versa
                    file_name = ''
                    if i % 2 == 0:
                        remove_temp('_temp1.wav')
                        file_name = '_temp1.wav'
                    else:
                        remove_temp('_temp2.wav')
                        file_name = '_temp2.wav'
                    # if os.path.isfile('_temp1.wav'):
                    #     remove_temp(file_name)
                    #     file_name = '_temp2.wav'

                    # install Microsoft Visual C++ 14.0+ to install simpleaudio to play music

                    file = AudioSegment.from_file(audio_path)
                    file.export(file_name, format='wav')

                    playsound(file_name)

            # remove_temp()

        def folder(argument, *values):
            """Plays audios from the whole folder."""
            self.check_values_length(folder.__name__, 1, *values)
            
            folder_path = values[0]
            if os.path.isdir(folder_path):
                dir_files = os.listdir(folder_path)
                audio_paths = self.get_files_paths(dir_files)
                audio_paths = [f'{folder_path}/{audio_path}' 
                    for audio_path in audio_paths]
                files(argument, *audio_paths)
            else:
                raise ValueError("Folder from the given path doesn't " +
                    "exist.")

        def randomize(argument, *values):
            """Turns on audio randomizing settings."""
            self.check_values_length(randomize.__name__, 0, *values)
            nonlocal randomize_play
            randomize_play = True

        arguments_list = {
            '-fs': files,
            '-f': folder,
            '-r': randomize
        }

        self.execute_arguments(command, arguments_list, '-fs')

    def copy(self, command):
        """Copies a file."""

        # Settings
        copy_path = 'copied/'
        copy_file_name = ''

        def file(argument, *values):
            """Copies file from the given path."""
            self.check_values_length(file.__name__, 1, *values)

            to_copy_path = values[0]
            destination_path = copy_path

            if not os.path.isdir(copy_path):
                os.mkdir(copy_path)

            if len(copy_file_name) > 0:
                destination_path += (f"/{copy_file_name}." +
                    f"{to_copy_path.split('.')[-1:][0]}")

            shutil.copy(to_copy_path, destination_path)

        def save(argument, *values):
            """Changes the default copy path."""
            self.check_values_length(save.__name__, 1, *values)
            nonlocal copy_path    
            copy_path = self.format_directory_path(values[0])

        def name(argument, *values):
            """Changes the default name of the copied file."""
            self.check_values_length(name.__name__, 1, *values)
            nonlocal copy_file_name    
            copy_file_name = values[0]

        arguments_list = {
            '-fe': file,
            '-s': save,
            '-n': name
        }

        self.execute_arguments(command, arguments_list, '-fe')

    def modify(self, command):
        """Modifies an audio file."""

        # Settings
        save_path = 'created/'
        file_name = datetime.datetime.now().strftime('%H_%M_%S_%Y_%m_%d')
        modifiers = {
            'speed': 1.0
        }

        def file(argument, *values):
            """Sets path to the file that has to be modified."""
            self.check_values_length(file.__name__, 1, *values)

            original_file_path = values[0]
            audio_file = AudioSegment.from_file(original_file_path)

            new_sample_rate = int(audio_file.frame_rate * modifiers['speed'])
            audio_file = audio_file._spawn(audio_file.raw_data, 
                overrides={'frame_rate': new_sample_rate})

            audio_file.export(f'{save_path}{file_name}.{original_file_path.split(".")[-1:][0]}')

        def save(argument, *values):
            """Changes default save path."""
            self.check_values_length(save.__name__, 1, *values)
            nonlocal save_path
            save_path = self.format_directory_path(values[0])

        def name(argument, *values):
            """Changes default output file name."""
            self.check_values_length(name.__name__, 1, *values)
            nonlocal file_name
            file_name = values[0]

        def speed(argument, *values):
            """
            Changes default speed of the file to modify.
            Note: speed value can be expressed as float or int
            """
            self.check_values_length(name.__name__, 1, *values)

            nonlocal modifiers
            speed_value = values[0]
            try:
                speed_value = float(speed_value)
            except:
                raise ValueError('Speed value must be an integer or a float.')

            modifiers['speed'] = speed_value

        arguments_list = {
            '-fe': file,
            '-s': save,
            '-n': name,
            '-sp': speed
        }

        self.execute_arguments(command, arguments_list, '')

def main():
    def help(command):
        help_arguments = {
            'general': MusicManagerHelp.help_general,
            'join': MusicManagerHelp.help_join,
            'play': MusicManagerHelp.help_play,
            'copy': MusicManagerHelp.help_copy,
            'modify': MusicManagerHelp.help_modify
        }

        command_index = sys.argv.index(command)
        argument = 'general'

        if command_index + 1 < len(sys.argv):
            argument = sys.argv[command_index + 1]

        if argument in help_arguments.keys():
            print(help_arguments[argument]())
        else:
            print(help_arguments['general']())

    musicManager = MusicManager(sys.argv)
    commands = {
        '-h': help,
        '-j': musicManager.join,
        '-p': musicManager.play,
        '-c': musicManager.copy,
        '-m': musicManager.modify
    }

    for command in commands.keys():
        if command in sys.argv:
            commands[command](command)
            break

if __name__ == '__main__':
    main()