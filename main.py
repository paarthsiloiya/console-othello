import time
from colorama import Fore, Style
from constants import BLACK, WHITE, EMPTY
from game_logic import create_board, is_game_over, get_winner, get_score, has_valid_move, apply_move
from ui import print_board, print_score, print_message, clear_screen, print_welcome
from player import get_human_move
from ai import get_best_move

def main():
    print_welcome()
    print("1. Player vs Player")
    print("2. Player vs Computer")
    
    while True:
        choice = input("Select mode (1 or 2): ").strip()
        if choice in ['1', '2']:
            break
        print("Invalid choice.")
        
    mode = int(choice)
    board = create_board()
    current_player = BLACK
    last_move_msg = ""
    
    while not is_game_over(board):
        clear_screen()
        print_board(board)
        black_score, white_score = get_score(board)
        print_score(black_score, white_score)
        if last_move_msg:
            print_message(last_move_msg)
            print()
        
        if not has_valid_move(board, current_player):
            if mode == 1:
                p_name = f"Player 1 ({Fore.RED}Black{Style.RESET_ALL})" if current_player == BLACK else f"Player 2 ({Fore.CYAN}White{Style.RESET_ALL})"
            else:
                p_name = f"Player ({Fore.RED}Black{Style.RESET_ALL})" if current_player == BLACK else f"Computer ({Fore.CYAN}White{Style.RESET_ALL})"
            
            print_message(f"{p_name} has no valid moves. Skipping turn.")
            time.sleep(2)
            current_player = WHITE if current_player == BLACK else BLACK
            continue
            
        if mode == 1:
            if current_player == BLACK:
                msg = f"Player 1's ({Fore.RED}Black{Style.RESET_ALL}) turn"
            else:
                msg = f"Player 2's ({Fore.CYAN}White{Style.RESET_ALL}) turn"
        else:
            if current_player == BLACK:
                msg = f"Player's ({Fore.RED}Black{Style.RESET_ALL}) turn"
            else:
                msg = f"Computer's ({Fore.CYAN}White{Style.RESET_ALL}) turn"
        
        print_message(msg)
        
        if mode == 1:
            row, col = get_human_move(board, current_player)
            col_char = chr(ord('A') + col)
            row_num = row + 1
            p_num = "1" if current_player == BLACK else "2"
            last_move_msg = f"Player {p_num} played: {col_char}{row_num}"
        else:
            if current_player == BLACK:
                row, col = get_human_move(board, current_player)
                col_char = chr(ord('A') + col)
                row_num = row + 1
                last_move_msg = f"Player played: {col_char}{row_num}"
            else:
                print_message("Computer is thinking...")
                move = get_best_move(board, current_player)
                if move:
                    row, col = move
                    col_char = chr(ord('A') + col)
                    row_num = row + 1
                    last_move_msg = f"Computer played: {col_char}{row_num}"
                else:
                    current_player = WHITE if current_player == BLACK else BLACK
                    continue
                    
        board = apply_move(board, row, col, current_player)
        current_player = WHITE if current_player == BLACK else BLACK
        
    clear_screen()
    print_board(board)
    black_score, white_score = get_score(board)
    print_score(black_score, white_score)
    
    winner = get_winner(board)
    if winner == BLACK:
        print_message("Black wins!")
    elif winner == WHITE:
        print_message("White wins!")
    else:
        print_message("It's a tie!")

if __name__ == "__main__":
    main()
