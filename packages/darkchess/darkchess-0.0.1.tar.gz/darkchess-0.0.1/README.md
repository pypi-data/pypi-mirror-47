# darkchess
### dark chess - incomplete information chess

Dark chess is a python package which has all the functionality of the game chess, with also a dark mode, where the player can only view the tiles of the board they are currently on or can move to.

This is an early version of the package. There are still bugs which are being worked on.

#### To install:
```
pip3 install darkchess
```

#### run.py

```
from darkchess.src.board import Board
from darkchess.src.gamengine import GameEngine
from darkchess.src.darkboard import DarkBoard

dark_mode = False
ans = ''
while 'y' not in ans and 'n' not in ans:
    ans = input("Do you want to play in dark mode? (y/n): ")

if 'y' in ans:
    dark_mode = True

if dark_mode:
    board = DarkBoard()
else:
    board = Board()
game = GameEngine(board)

while True:
    # game.Board.view_board_debug()
    game.Board.view_board()
    # if dark_mode:
    # game.Board.view_board_true_sight()
    game.choose_move()
```

#### To run tests:
```
pytest --pyargs darkchess
```