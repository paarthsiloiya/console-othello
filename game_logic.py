from constants import BOARD_SIZE, EMPTY, BLACK, WHITE

def create_board():
    """
    Creates and initializes the game board.

    Returns:
        list: A 2D list representing the 8x8 Othello board with the initial four pieces placed in the center.
    """
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    mid = BOARD_SIZE // 2
    board[mid-1][mid-1] = WHITE
    board[mid][mid] = WHITE
    board[mid-1][mid] = BLACK
    board[mid][mid-1] = BLACK
    return board

def is_on_board(r, c):
    """
    Checks if the given coordinates are within the board boundaries.

    Args:
        r (int): The row index.
        c (int): The column index.

    Returns:
        bool: True if the coordinates are valid, False otherwise.
    """
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

def is_valid_move(board, row, col, player):
    """
    Determines if a move is valid for a given player at a specific location.

    A move is valid if:
    1. The cell is empty.
    2. It outflanks at least one opponent piece in any of the 8 directions.

    Args:
        board (list): The current game board.
        row (int): The row index of the move.
        col (int): The column index of the move.
        player (str): The color of the player making the move (BLACK or WHITE).

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if board[row][col] != EMPTY:
        return False
    
    opponent = WHITE if player == BLACK else BLACK
    
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if is_on_board(r, c) and board[r][c] == opponent:
            r += dr
            c += dc
            while is_on_board(r, c):
                if board[r][c] == player:
                    return True
                if board[r][c] == EMPTY:
                    break
                r += dr
                c += dc
            
    return False

def get_valid_moves(board, player):
    """
    Returns a list of all valid moves for the given player.

    Args:
        board (list): The current game board.
        player (str): The color of the player (BLACK or WHITE).

    Returns:
        list: A list of tuples (row, col) representing valid move coordinates.
    """
    moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if is_valid_move(board, r, c, player):
                moves.append((r, c))
    return moves

def apply_move(board, row, col, player):
    """
    Applies a move to the board and flips the captured pieces.

    Args:
        board (list): The current game board.
        row (int): The row index of the move.
        col (int): The column index of the move.
        player (str): The color of the player making the move.

    Returns:
        tuple: A tuple containing:
            - new_board (list): The new board state after the move.
            - flipped_groups (list): A list of lists, where each inner list contains the coordinates of pieces flipped in a particular direction.
    """
    new_board = [row[:] for row in board]
    new_board[row][col] = player
    opponent = WHITE if player == BLACK else BLACK
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    
    flipped_groups = []
                  
    for dr, dc in directions:
        r, c = row + dr, col + dc
        to_flip = []
        while is_on_board(r, c) and new_board[r][c] == opponent:
            to_flip.append((r, c))
            r += dr
            c += dc
        if is_on_board(r, c) and new_board[r][c] == player:
            if to_flip:
                flipped_groups.append(to_flip)
                for fr, fc in to_flip:
                    new_board[fr][fc] = player
                
    return new_board, flipped_groups

def has_valid_move(board, player):
    """
    Checks if the player has at least one valid move.

    Args:
        board (list): The current game board.
        player (str): The color of the player.

    Returns:
        bool: True if the player has a valid move, False otherwise.
    """
    return len(get_valid_moves(board, player)) > 0

def is_game_over(board):
    """
    Checks if the game is over (i.e., neither player can move).

    Args:
        board (list): The current game board.

    Returns:
        bool: True if the game is over, False otherwise.
    """
    return not has_valid_move(board, BLACK) and not has_valid_move(board, WHITE)

def get_score(board):
    """
    Calculates the current score for both players.

    Args:
        board (list): The current game board.

    Returns:
        tuple: A tuple (black_score, white_score).
    """
    black_score = sum(row.count(BLACK) for row in board)
    white_score = sum(row.count(WHITE) for row in board)
    return black_score, white_score

def get_winner(board):
    """
    Determines the winner of the game.

    Args:
        board (list): The current game board.

    Returns:
        str: The color of the winner (BLACK or WHITE), or EMPTY if it's a tie.
    """
    black, white = get_score(board)
    if black > white:
        return BLACK
    elif white > black:
        return WHITE
    else:
        return EMPTY
