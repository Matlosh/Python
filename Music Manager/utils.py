import textwrap

class ArgumentError(Exception):
    """
    Extension of Exception class.
    Allows to throw an error related to wrong number of provided arguments.
    """

    def __init__(self, function_name, provided_args, expected_args):
        super().__init__()
        self.function_name = function_name
        self.provided_args = provided_args
        self.exepcted_args = expected_args

    def __str__(self):
        provided_args_str = 'argument' if self.provided_args == 1 else 'arguments'
        expected_args_str = 'argument' if self.exepcted_args == 1 else 'arguments'
        return (f'{self.function_name} needs {self.exepcted_args}'
            f' {expected_args_str}, but ' + f'{self.provided_args}'
            f' {provided_args_str} were provided.')

class FolderNotFoundError(Exception):
    """
    Extension of Exception class.
    Allows to throw an error related to not existing path to a folder.
    """

    def __init__(self, message='Provided path to the folder is wrong.'):
        super().__init__(message)

class MusicManagerHelp:

    @staticmethod
    def help_general():
        help = """
        Help:

        Available commands:
            -j -> joins multiple audio files into one
                available arguments: [-fs, -s, -n, -f, -g, -rft, -b, -cr]
            -p -> plays audio from a file
                available arguments: [-fs, -f, -r]
            -c -> copies a file
                available arguments: [-fe, -s, -n]
            -m -> modifies an audio file
                available arguments: [-fe, -s, -n, -sp]

        For more information about each command, use: -h [join/play/copy/modify]"""

        return textwrap.dedent(help)

    @staticmethod
    def help_join():
        help = """
        Help for join:

        Description:
            Join command allows to join multiple audio files into one and add
            simple settings such as crossfade between audios or gap.

        Arguments:
            -fs -> joins audio files from given paths
                values: [one or many paths to the audio files]
            -s -> changes the default path of a folder where joined 
                audio will be saved
                value: [path to a folder]
            -n -> changes default name of the output file
                value: [name of the file]
            -f -> joins all audio files from the given path to a folder
                value: [path to a folder]
            -g -> adds gap between each joined audio
                value: [gap duration in milliseconds]
            -rft -> changes default type of the output file
                value: [file type]
            -b -> changes default bitrate of the output file
                value: [bitrate]
            -cr -> adds crossfade effect between each joined audio
                value: [crossfade duration in milliseconds]"""

        return textwrap.dedent(help)

    @staticmethod
    def help_play():
        help = """
        Help for play:

        Description:
            Play command allows to play audio file in a terminal, providing
            simple settings such as randomizing the order of playing or
            playing the audios from the whole folders.

        Arguments:
            -fs -> plays audio file/files from given path/paths
                values: [one or many paths to the audio files]
            -f -> plays all audio files from the given path to a folder
                value: [path to a folder]
            -r -> randomizes the order of audio files that will be played
                value: None"""

        return textwrap.dedent(help)

    @staticmethod
    def help_copy():
        help = """
        Help for copy:

        Description:
            Copy command as the name suggests, allows to copy a file with possibility
            of changing the name or save path of the output file.

        Arguments:
            -fe -> copies file from the given path
                value: [path to a file]
            -s -> changes the default path of a folder where the output
                file will be saved
                value: [path to a folder]
            -n -> changes the default name of the output file
                value: [output file name]"""

        return textwrap.dedent(help)

    @staticmethod
    def help_modify():
        help = """
        Help for modify:

        Description:
            Modify command allows to modify few of the audio file settings
            such as speed.

        Arguments:
            -fe -> modifies the file with all set settings and saves it
                value: [path to a file]
            -s -> changes the default path of a folder where the output
                file will be saved
                value: [path to a folder]
            -n -> changes the default name of the output file
                value: [output file name]
            -sp: -> modifies speed of the audio file
                value: [speed value in float or int]"""

        return textwrap.dedent(help)