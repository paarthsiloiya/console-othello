# AI Documentation

This document explains the current AI implementation for the Console Othello game and provides suggestions for future improvements.

## Current Implementation

The AI uses a **MinMax Algorithm** to decide its moves. This is a recursive algorithm used for decision-making in game theory and artificial intelligence.

### How it Works

1.  **Search Tree**: The AI simulates future game states by exploring possible moves for itself and the opponent.
2.  **Depth**: The algorithm looks ahead a fixed number of turns (currently set to **3**).
    *   Depth 0: The current board state.
    *   Depth 1: All possible moves for the AI.
    *   Depth 2: All possible responses by the opponent.
    *   Depth 3: All possible counter-responses by the AI.
3.  **Evaluation Function**: At the maximum depth (leaf nodes) or if the game ends, the board state is evaluated to give it a numerical score.
    *   **Maximizing Player (AI)**: Tries to choose the move that leads to the highest score.
    *   **Minimizing Player (Human)**: Assumed to play optimally, choosing the move that leads to the lowest score for the AI.

### Heuristics

The current evaluation function (`evaluate_board` in `ai.py`) uses a simple heuristic:

1.  **Piece Count**: The basic score is the difference between the AI's pieces and the opponent's pieces.
2.  **Corner Control**: Corners are extremely valuable in Othello because they cannot be flipped once taken.
    *   The AI assigns a bonus of **25 points** for owning a corner.
    *   This encourages the AI to prioritize moves that secure corners.

### Alpha-Beta Pruning

The implementation includes **Alpha-Beta Pruning** optimization. This significantly reduces the number of nodes evaluated in the search tree by stopping the evaluation of a move when at least one possibility has been found that proves the move to be worse than a previously examined move.

## How to Improve the AI

The current AI is competent but basic. Here are several ways to make it stronger:

### 1. Better Heuristics (Evaluation Function)
The current function relies heavily on piece count, which is actually a poor metric in the early and mid-game of Othello. Better metrics include:

*   **Mobility**: The number of valid moves available to a player. Forcing the opponent into a state with few moves is a strong strategy.
*   **Stability**: Pieces that can never be flipped (e.g., corners and edges connected to corners) are "stable".
*   **Edge Play**: Assign different weights to different squares. For example, the squares immediately adjacent to corners (C-squares and X-squares) are often dangerous to take and should have negative weights.
*   **Parity**: In the endgame, having the last move in a region is advantageous.

### 2. Dynamic Weighting
The importance of different heuristics changes throughout the game.
*   **Opening/Mid-game**: Prioritize Mobility and Positional Strategy (avoiding bad squares).
*   **Endgame**: Prioritize Piece Count (Coin Parity).

### 3. Increased Search Depth
*   Increasing the depth from 3 to 5 or 6 will make the AI significantly smarter but slower.
*   Optimizing the code or using a faster language (like C++) would allow for deeper searches.

### 4. Iterative Deepening
Instead of a fixed depth, the AI can search to depth 1, then depth 2, etc., within a time limit. This ensures the AI always has a move ready if time runs out.

### 5. Transposition Table
Store board states that have already been evaluated to avoid re-calculating them if the search reaches the same position via a different sequence of moves.

### 6. Opening Book
Use a database of standard opening moves to play perfectly for the first few turns, saving computation time and avoiding early traps.

### 7. Endgame Solver
When there are few empty squares left (e.g., 10-12), the AI can switch to a "perfect" solver that searches to the very end of the game to find the absolute best sequence of moves to win.
