# AI Documentation

This document explains the AI implementations for the Console Othello game.

## Improved AI (`new_ai.py`)

The default AI for the game is now a significantly more advanced agent that uses several techniques to play at a high level.

### Core Algorithm
*   **MinMax with Alpha-Beta Pruning**: The foundation is still the standard MinMax algorithm optimized with Alpha-Beta pruning to cut off irrelevant branches of the search tree.
*   **Iterative Deepening**: Instead of searching to a fixed depth, the AI searches to depth 1, then depth 2, and so on, until a time limit (2 seconds) is reached. This ensures the AI always has a valid move ready and uses its time efficiently.

### Evaluation Function (Heuristics)
The AI evaluates board states using a weighted combination of three factors, which changes dynamically based on the game phase (Opening, Midgame, Endgame):

1.  **Positional Strategy (Static Weights)**:
    *   The board is mapped to a grid of weights.
    *   **Corners** are highly valued (+100).
    *   **C-squares and X-squares** (adjacent to corners) are penalized (-20, -50) to avoid giving corners to the opponent.
    *   Edges are slightly positive.

2.  **Mobility**:
    *   The AI attempts to maximize its own number of valid moves while minimizing the opponent's options.
    *   This forces the opponent into bad positions.

3.  **Coin Parity**:
    *   Simply having more pieces than the opponent.
    *   This is given very low weight in the opening/midgame but becomes the primary factor in the endgame.

### Endgame Solver
When there are **10 or fewer empty squares** remaining, the AI switches to a "perfect" solver. It searches the entire remaining game tree to find the absolute best sequence of moves to win the game, ignoring the time limit if necessary to ensure victory.

---

## Legacy AI (`old_ai.py`)

The original AI is kept for comparison and benchmarking purposes.

*   **Algorithm**: Fixed-depth MinMax (Depth 3).
*   **Heuristics**: Simple piece count + Corner bonus (25 points).
*   **Weakness**: It is greedy for pieces early in the game, which is often a losing strategy in Othello.

## Future Improvements

While the new AI is strong, it can still be improved:

1.  **Transposition Table**: Store evaluated board states to avoid re-calculating the same position reached via different move orders.
2.  **Opening Book**: Use a database of standard openings to play instantly and perfectly for the first 10-15 moves.
3.  **Pattern Recognition**: Instead of static weights, recognize specific edge and corner patterns (e.g., "Stoner Trap").
4.  **MCTS (Monte Carlo Tree Search)**: An alternative to MinMax that can be very effective, especially when combined with neural networks (like AlphaZero).
