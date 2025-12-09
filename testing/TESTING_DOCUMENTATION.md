# Testing and Benchmarking Documentation

This folder contains tools to benchmark and analyze the performance of different AI implementations for Console Othello.

## Folder Structure

*   `benchmark.py`: The main script to run simulations.
*   `analysis.ipynb`: A Jupyter Notebook to visualize and analyze the results.
*   `old_ai.py`: A copy of the legacy AI (08-12-2025).
*   `new_ai.py`: A copy of the improved AI (Iterative Deepening, Advanced Heuristics, Bitboard Optimization, Opening Book).
*   `benchmark_games.csv`: (Generated) Contains summary data for each simulated game.
*   `benchmark_moves.csv`: (Generated) Contains detailed data for every move in every game.

## How to Run a Benchmark

1.  **Install Dependencies**:
    Ensure you have `tqdm` installed:
    ```bash
    pip install tqdm
    ```

2.  **Run the Script**:
    Execute the benchmark script from the project root:
    ```bash
    python testing/benchmark.py
    ```
    
    *   **What it does**:
        *   Simulates **100 games** between `old_ai` and `new_ai`.
        *   **Phase 1 (Games 1-50)**: Old AI plays Black (First), New AI plays White.
        *   **Phase 2 (Games 51-100)**: New AI plays Black (First), Old AI plays White.
        *   Displays a progress bar with estimated completion time.
    
    *   **Output**:
        *   Generates `testing/benchmark_games.csv` and `testing/benchmark_moves.csv`.

## How to Analyze Results

1.  **Open the Notebook**:
    Open `testing/analysis.ipynb` in VS Code or Jupyter Lab.

2.  **Run All Cells**:
    Execute all cells in the notebook to generate reports and visualizations.

3.  **Available Analysis**:
    *   **Overall Win Rate**: Pie chart showing the dominance of the New AI.
    *   **Win Rate per Phase**: Bar chart comparing performance when moving first vs. second.
    *   **Game Duration**: Histogram of how long games take (in seconds).
    *   **Move Time Analysis**: Comparison of average thinking time for both AIs.
    *   **Move Time Progression**: Line graph showing how thinking time changes as the game progresses (demonstrating the effect of Iterative Deepening and the Endgame Solver).
