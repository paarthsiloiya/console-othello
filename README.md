# Console Othello

A clean, console-based implementation of the classic board game Othello (also known as Reversi) in Python.

## Features

*   **Two Game Modes**:
    *   **Player vs Player**: Play against a friend on the same computer.
    *   **Player vs Computer**: Challenge an AI opponent.
*   **Visuals**:
    *   Uses Unicode box-drawing characters for a crisp board display.
    *   Colored pieces (Red for Black, Cyan for White) for easy distinction.
    *   Clear screen updates for a smooth experience.
*   **Advanced AI**:
    *   **Bitboard Representation**: Utilizes 64-bit integers for board state, enabling extremely fast bitwise operations for move generation and validation.
    *   **Opening Book**: Includes a database of standard opening moves to play perfectly in the early game.
    *   **MinMax with Alpha-Beta Pruning**: Efficiently searches the game tree to find optimal moves.
    *   **Iterative Deepening**: Searches progressively deeper within a time limit to ensure the best possible move is found within the allocated time.
    *   **Heuristic Evaluation**: Evaluates board states based on positional weight maps, mobility (number of valid moves), and coin parity.
    *   **Endgame Solver**: Switches to an exact search when few empty squares remain to calculate the perfect sequence of moves.

## Documentation

The project code is fully documented using Google-style docstrings. You can view the hosted documentation here:

**[Console Othello Documentation](https://paarthsiloiya.github.io/console-othello/)**

You can also generate the documentation locally using Sphinx.

The documentation is produced by AI.

### Generating Documentation

1.  Install Sphinx and the theme:
    ```bash
    pip install sphinx shibuya
    ```
2.  Navigate to the `docs` directory (create it if it doesn't exist and run `sphinx-quickstart`).
3.  Run the build command:
    ```bash
    make html
    ```
4.  Open `docs/_build/html/index.html` in your browser.

## Requirements

*   Python 3.x
*   `colorama` library
*   `bext` library (for animations)
*   `tqdm` library (for benchmarking)

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/paarthsiloiya/console-othello.git
    cd console-othello
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## How to Play

1.  Run the game:
    ```bash
    python main.py
    ```

2.  Select a game mode from the menu.

3.  **Controls**:
    *   Enter your move using the column letter and row number (e.g., `C4`, `D3`).
    *   Black (Player 1) always moves first.

## Rules

*   The game is played on an 8x8 board.
*   Players take turns placing a disk of their color on the board.
*   A valid move must "outflank" at least one opponent's disk. This means trapping opponent disks between the new disk and another disk of your color already on the board.
*   Trapped disks are flipped to your color.
*   If a player has no valid moves, their turn is skipped.
*   The game ends when neither player can move.
*   The player with the most disks on the board wins.

## Project Structure

*   `main.py`: Entry point of the game.
*   `game_logic.py`: Core game rules and mechanics.
*   `ai.py`: Advanced AI implementation (Bitboards, MinMax, Opening Book).
*   `opening_book.py`: Opening book logic and data.
*   `ui.py`: User interface and display logic.
*   `player.py`: Input handling for human players.
*   `constants.py`: Global constants and configuration.
*   `testing/`: Contains benchmarking tools and analysis notebooks.
