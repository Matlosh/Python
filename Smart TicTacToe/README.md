# Smart TicTacToe

*Are you ready to train and play with your TicTacToe?*

## About

Have you always dreamt of having your own TicTacToe pet?

No? *Well, me neither*

But with this short program you can gather games data to the dataset file and *maybe by some miracle* TicTacToe CPU will try to use that data to make some *smart* moves!

## Usage

Usage vary from the app functions you want to use.

### Simple usage

If you want to just play simple TicTacToe use command:

```
python main.py
```

### Training mode

If you want to train your TicTacToe CPU (through saving randomly generated games results) use command:

```
python main.py -t=1000
```

*(where 1000 can be replaced with number of results that have to be generated and inserted into the dataset file)*

### Using datasets

If you want to use (or firstly create) dataset file you can use command:

```
python main.py -dp=mydataset
```

*(where mydataset can be replaced with any path to json file - lack of path before dataset filename means dataset is located in default path)*

### Combined

Training mode and custom datasets can be combined:

```
python main.py -dp=mydataset -t=1000
```

## Help

Help can be reached by using the following command:

```
python main.py -h
```
