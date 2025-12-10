from constants import BOARD_SIZE
from game_logic import is_valid_move

def get_human_move(board, player):
    """
    Prompts the human player for a move and validates it.

    Args:
        board (list): The current game board.
        player (str): The color of the current player.

    Returns:
        tuple: The coordinates (row, col) of the valid move entered by the user.
    """
    while True:
        try:
            move_str = input(f"Enter move (e.g. C4): ").strip().upper()
            if len(move_str) < 2:
                print("Invalid format. Use ColumnRow (e.g. C4).")
                continue
                
            col_char = move_str[0]
            row_str = move_str[1:]
            
            if not col_char.isalpha() or not row_str.isdigit():
                print("Invalid format. Use ColumnRow (e.g. C4).")
                continue
                
            col = ord(col_char) - ord('A')
            row = int(row_str) - 1
            
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                if is_valid_move(board, row, col, player):
                    return (row, col)
                else:
                    print("Invalid move. Try again.")
            else:
                print("Move out of bounds.")
                
        except ValueError:
            print("Invalid input.")
