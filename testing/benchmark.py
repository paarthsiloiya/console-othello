import sys
import os
import time
import csv
import random
from tqdm import tqdm

# Add parent directory to path so we can import game_logic and constants
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import BLACK, WHITE, EMPTY, BOARD_SIZE
from game_logic import create_board, is_game_over, get_winner, get_score, has_valid_move, apply_move

# Import AIs
# We need to make sure they can import game_logic/constants from parent too
# Since we added parent to sys.path, it should work.
import testing.old_ai as old_ai
import testing.new_ai as new_ai

def play_game(game_id, phase):
    board = create_board()
    current_player = BLACK
    
    # Phase 1: Old AI is Black (First), New AI is White
    # Phase 2: New AI is Black (First), Old AI is White
    
    if phase == 1:
        black_player = "Old AI"
        white_player = "New AI"
    else:
        black_player = "New AI"
        white_player = "Old AI"
        
    game_moves = []
    start_time = time.time()
    move_count = 0
    
    while not is_game_over(board):
        if not has_valid_move(board, current_player):
            current_player = WHITE if current_player == BLACK else BLACK
            if not has_valid_move(board, current_player):
                break
            continue
            
        move_start = time.time()
        
        if current_player == BLACK:
            player_type = black_player
        else:
            player_type = white_player
            
        if player_type == "Old AI":
            move = old_ai.get_best_move(board, current_player, time_limit=1)
        else:
            move = new_ai.get_best_move(board, current_player, time_limit=1)
            
        move_end = time.time()
        move_duration = move_end - move_start
        move_count += 1
        
        game_moves.append({
            "game_id": game_id,
            "move_number": move_count,
            "player_type": player_type,
            "move_time": move_duration
        })
        
        if move:
            # Handle different return types if necessary (new AI returns just move, apply_move returns board, flipped)
            # But get_best_move just returns (r, c) for both.
            # apply_move signature might differ?
            # game_logic.apply_move returns (new_board, flipped_groups) now.
            # We need to handle that.
            board, _ = apply_move(board, move[0], move[1], current_player)
        else:
            # Should not happen if has_valid_move is true, but just in case
            pass
            
        current_player = WHITE if current_player == BLACK else BLACK
        
    end_time = time.time()
    total_time = end_time - start_time
    
    winner_color = get_winner(board)
    if winner_color == BLACK:
        winner = black_player
    elif winner_color == WHITE:
        winner = white_player
    else:
        winner = "Tie"
        
    black_score, white_score = get_score(board)
    
    game_data = {
        "game_id": game_id,
        "phase": phase,
        "winner": winner,
        "total_time": total_time,
        "black_score": black_score,
        "white_score": white_score,
        "black_player": black_player,
        "white_player": white_player
    }
    
    return game_data, game_moves

def main():
    num_games = 100
    games_data = []
    all_moves_data = []
    
    print(f"Starting benchmark of {num_games} games...")
    
    for i in tqdm(range(1, num_games + 1), desc="Simulating Games", unit="game"):
        if i <= 50:
            phase = 1
        else:
            phase = 2
            
        # print(f"Playing Game {i}/{num_games} (Phase {phase})...")
        game_data, moves_data = play_game(i, phase)
        
        games_data.append(game_data)
        all_moves_data.extend(moves_data)
        
    # Save to CSV
    print("Saving results...")
    
    with open('testing/benchmark_games.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["game_id", "phase", "winner", "total_time", "black_score", "white_score", "black_player", "white_player"])
        writer.writeheader()
        writer.writerows(games_data)
        
    with open('testing/benchmark_moves.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["game_id", "move_number", "player_type", "move_time"])
        writer.writeheader()
        writer.writerows(all_moves_data)
        
    print("Benchmark complete.")

if __name__ == "__main__":
    main()
