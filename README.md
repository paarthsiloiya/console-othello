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
*   **AI**:
    *   Implements a MinMax algorithm to determine the best moves.

## Requirements

*   Python 3.x
*   `colorama` library

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
*   `ai.py`: AI implementation (MinMax algorithm).
*   `ui.py`: User interface and display logic.
*   `player.py`: Input handling for human players.
*   `constants.py`: Global constants and configuration.
