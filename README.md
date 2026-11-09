# Checkers with an AI Opponent

A checkers game built with Python and Pygame. Play as the red side against a
white AI opponent that searches moves with Minimax and Alpha-Beta pruning. The
board uses an ivory and forest-green palette, with burgundy and ivory pieces for
clear contrast.

## Requirements

- Python 3
- Pygame, or the compatible `pygame-ce` community edition

Install one of the supported Pygame packages:

```bash
python -m pip install pygame
```

Or, to use the community edition:

```bash
python -m pip install pygame-ce
```

## Run the Game

From the project root (the directory containing `main.py`), run:

```bash
python main.py
```

Run from the project root so the crown image at `assets/assets/crown.png` is
found.

## How to Play

1. Click a red checker to select it.
2. Click a highlighted square to move. Captured pieces are removed when the
   chosen move is a capture.
3. The white AI makes its move automatically after the red player.
4. The game ends when a side has no pieces or the player whose turn it is has
   no legal moves.

## AI

The white AI uses depth-limited Minimax to choose a move. Alpha-Beta pruning
skips branches that cannot change the final choice. Heuristic move ordering
searches promising boards first, helping pruning become effective earlier.
Board evaluation scores piece counts and gives kings additional value.

To adjust how far ahead the AI searches, change `DEPTH` near the top of
`main.py`. Increasing the depth may make the AI's turns take longer.

## Project Structure

```text
.
├── assets/
│   └── assets/
│       └── crown.png
├── checker/
│   ├── minimax/
│   │   └── algorithm.py
│   ├── board.py
│   ├── constants.py
│   ├── game.py
│   └── piece.py
└── main.py
```
