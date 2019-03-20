# Blockus (Not Blokus)
[Blockus Game Rules](https://en.wikipedia.org/wiki/Blokus)

## Modules
```main.py```: Driver of game without blockus environment/server support. Runs simple game with random moves chosen. Call ```python main.py show``` to render pygame board and ```python main.py``` to see terminal output (which is faster).

```board.py```: Handles state of hte board, piece placements, and valid move driver methods.

```computation.py```: Contains computation methods that ```board.py``` uses to manage valid move seeks and piece placement. Methods use Numba with jit decorator that precompiles
  types and makes runtime faster than normal python.
 
```ai.py```: Keeps track of player score, inventory, and returns all valid moves for that specific player.

```gui.py```: Utlizes Pygame to show pieces getting placed on board as a visual cue. When enabled, the gui slows computation time signifigantly. We recomend you 
disable the gui for agent training. 

## Valid Moves
```piece_type```: Blockus has 20 playable pieces. Each player name is defined in a dictionary in blockus/board.py

```index```: The index is a cell on the board where the piece can be rotated and flipped around. 

```orientation```: Orientation the piece is in. The piece can be flipped in the x and y direction in each of the 8 different orientations the ```piece_type``` can be in.

```shifted_id```: For each piece type, index, and orientation, the piece can be shifted N times where N is how many cells the current piece takes up

Valid moves are stored in a combination of dictionary lists providing O(1) valid move lookup

