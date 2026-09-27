# Terminal Chess

A from-scratch, two-player chess game for the command line, written in **Python 3** using only the standard library.

The project focuses on implementing the **rules of chess**, rather than building an AI engine that searches for the best move. The main goal is to turn chess rules into clear, testable Python logic.

> **AI Development Note:** *Phase 3 and the restructure of the whole project was done by AI.*

## Overview

Terminal Chess runs entirely in a text terminal. Two players share the same keyboard, entering moves such as `e2e4` until the game ends by checkmate, stalemate, or the player choosing to exit.

The project is intentionally built without external chess libraries so that the core rules and data flow remain visible.

### Main goals

- **Correctness over optimization** — the rules are implemented directly and readably.
- **Separation of responsibilities** — board state, chess rules, messages, and game flow are kept in separate modules.
- **Safe move validation** — hypothetical moves are tested on cloned boards so illegal self-checks never modify the real position.
- **Clear terminal interaction** — the board is redrawn each turn instead of producing a long scrolling history.

## Features

The rules engine currently handles:

- Normal movement for king, queen, rook, bishop, knight, and pawn
- Path blocking for sliding pieces
- Capturing and friendly-piece protection
- Turn validation
- Check detection
- Checkmate detection
- Stalemate detection
- Castling
- En passant
- Pawn promotion to queen, rook, bishop, or knight
- Algebraic move notation for move history
- Undo
- Save/load game state using JSON
- Built-in help and human-readable error messages
- Cross-platform terminal clearing for Windows and Unix-like systems

## Architecture

The project is split into four files, with each module having a focused responsibility:

```text
main.py
  │
  ▼
pieces.py
  │
  ▼
board.py

errors.py  ── shared message constants
```

| File | Responsibility |
|---|---|
| `board.py` | Creates, displays, clears, and clones the board |
| `pieces.py` | Implements movement rules, attacks, checks, special moves, and legality |
| `errors.py` | Stores user-facing error/status messages and help text |
| `main.py` | Runs the game loop, reads input, applies legal moves, and manages game state |

This separation also means the rules engine does not depend on the terminal interface. In principle, `pieces.py` could be reused behind a graphical interface, web interface, or automated test suite.

## How the Board Is Represented

The board is a simple **8×8 list of lists**:

```python
board[row][col]
```

Pieces are represented by single characters:

| Character | Meaning |
|---|---|
| `0` | Empty square |
| `K Q R B N P` | White pieces |
| `k q r b n p` | Black pieces |

The board uses:

- Row `0` → rank `8`
- Row `7` → rank `1`
- Column `0` → file `A`
- Column `7` → file `H`

So the conversion between chess ranks and board rows is:

```text
row = 8 - rank
```

The project also keeps game information that cannot be inferred from the board alone:

- `castling_rights`
- `en_passant_target`

These are treated as part of the complete game state and are preserved by undo/save/load.

## The Rules Engine

`pieces.py` is the core of the project.

Its logic is layered from small helpers to complete move validation:

```text
Coordinate parsing
       ↓
Geometry / path checks
       ↓
Piece movement rules
       ↓
Attack + check detection
       ↓
Hypothetical move simulation
       ↓
Special moves
       ↓
is_legal_move()
       ↓
Checkmate / stalemate detection
```

### Key idea: `is_legal_move()`

The central question is:

> **"Is this move legal in the current position?"**

A move must pass several levels of validation:

1. The input represents valid board coordinates.
2. A piece exists on the starting square.
3. The piece belongs to the player whose turn it is.
4. The destination is not occupied by a friendly piece.
5. The piece's movement pattern is valid.
6. Sliding pieces have a clear path.
7. Special rules such as castling or en passant are satisfied.
8. The move does **not leave the moving player's own king in check**.

That last step is handled by **simulating the move on a cloned board** instead of modifying the real board.

### Why simulation matters

When the engine needs to ask "what would happen if this move were played?", it:

```text
Real board
   │
   ├── clone
   ▼
Hypothetical board
   │
   ├── apply move
   ├── inspect king safety
   ▼
Discard clone
```

This makes it possible to safely test moves for:

- Self-check
- Checkmate searches
- Stalemate searches

The real board is changed only after legality has already been confirmed.

## Special Rules

### Castling

Castling checks all required conditions, including:

- The king and relevant rook have not moved.
- The squares between them are empty.
- The king is not currently in check.
- The king does not cross an attacked square.
- The king does not finish on an attacked square.

The game also accepts conventional castling input:

```text
O-O
O-O-O
```

and the `0-0` / `0-0-0` variants.

### En Passant

The engine tracks an `en_passant_target` square after a pawn makes a two-square advance. The opportunity exists only for the immediately following move.

### Promotion

A pawn reaching the final rank must immediately become one of:

```text
Queen
Rook
Bishop
Knight
```

The player's choice is requested before the turn finishes.

## Game Commands

During a game, the terminal accepts commands such as:

| Command | Action |
|---|---|
| `e2e4` | Move a piece |
| `O-O` / `O-O-O` | Castle |
| `undo` | Undo the previous move |
| `history` | Show move history |
| `save [filename]` | Save the current game |
| `load [filename]` | Load a saved game |
| `help` | Show command help |
| `exit` | Quit the game |

The default save file is `chess_save.json` when no filename is supplied.

## Game-State Management

The main loop keeps the complete state of a game:

```python
board
turn
move_history
undo_stack
castling_rights
en_passant_target
status_message
```

Undo works by restoring a complete snapshot instead of trying to reverse individual changes manually.

Save/load serializes the relevant state to JSON, including castling rights and the en passant target.

## Error Handling

User-facing messages are centralized in `errors.py`.

Instead of printing directly from the rules engine, validation functions return a result and a reason. This allows the same rules code to be called silently during hypothetical move searches without flooding the terminal with irrelevant messages.

The restructure also fixed several issues, including:

- Inconsistent `(row, col)` argument ordering
- Inconsistent return types from movement checks
- Messages being printed during silent legality scans
- Invalid ranks silently wrapping around Python list indices
- The terminal continuously scrolling instead of presenting a single current board

The most important historical bug came from swapping row and column arguments when checking which player owned a piece, causing even the opening move `e2e4` to be rejected.

## Project Structure

```text
.
├── board.py
├── pieces.py
├── errors.py
├── main.py
└── chess_save.json   # created when a game is saved
```

## Learning Focus

This project is primarily a study exercise in:

- Translating real-world rules into program logic
- Working with nested Python lists
- Coordinate systems and indexing
- Function decomposition
- Separation of concerns
- State management
- Defensive input validation
- Simulation of hypothetical states
- Recursive/exhaustive legality checks
- Designing reusable rule logic

It deliberately avoids more advanced chess-engine techniques such as bitboards, opening books, and move-search optimization.

## Possible Extensions

The current rules engine can be extended with:

- Threefold-repetition detection
- The fifty-move rule
- More complete algebraic notation disambiguation
- PGN export
- Unicode chess pieces in the terminal
- A chess-playing AI
- A graphical, web, or automated-test interface

Because the terminal-specific logic is isolated in `main.py`, these extensions can be built without rewriting the core movement rules.

