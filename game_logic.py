from constants import BOARD_SIZE, EMPTY, BLACK, WHITE

def create_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    mid = BOARD_SIZE // 2
    board[mid-1][mid-1] = WHITE
    board[mid][mid] = WHITE
    board[mid-1][mid] = BLACK
    board[mid][mid-1] = BLACK
    return board

def is_on_board(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

def is_valid_move(board, row, col, player):
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
    moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if is_valid_move(board, r, c, player):
                moves.append((r, c))
    return moves

def apply_move(board, row, col, player):
    new_board = [row[:] for row in board]
    new_board[row][col] = player
    opponent = WHITE if player == BLACK else BLACK
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
                  
    for dr, dc in directions:
        r, c = row + dr, col + dc
        to_flip = []
        while is_on_board(r, c) and new_board[r][c] == opponent:
            to_flip.append((r, c))
            r += dr
            c += dc
        if is_on_board(r, c) and new_board[r][c] == player:
            for fr, fc in to_flip:
                new_board[fr][fc] = player
                
    return new_board

def has_valid_move(board, player):
    return len(get_valid_moves(board, player)) > 0

def is_game_over(board):
    return not has_valid_move(board, BLACK) and not has_valid_move(board, WHITE)

def get_score(board):
    black_score = sum(row.count(BLACK) for row in board)
    white_score = sum(row.count(WHITE) for row in board)
    return black_score, white_score

def get_winner(board):
    black, white = get_score(board)
    if black > white:
        return BLACK
    elif white > black:
        return WHITE
    else:
        return EMPTY
