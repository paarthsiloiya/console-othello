from constants import BLACK, WHITE, BOARD_SIZE, EMPTY
from game_logic import get_valid_moves, apply_move, is_game_over, get_score

def evaluate_board(board, player):
    opponent = WHITE if player == BLACK else BLACK
    
    my_score = 0
    op_score = 0
    
    corners = [(0, 0), (0, BOARD_SIZE-1), (BOARD_SIZE-1, 0), (BOARD_SIZE-1, BOARD_SIZE-1)]
    
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == player:
                my_score += 1
                if (r, c) in corners:
                    my_score += 25
            elif board[r][c] == opponent:
                op_score += 1
                if (r, c) in corners:
                    op_score += 25
                    
    return my_score - op_score

def minmax(board, depth, maximizing_player, player, alpha, beta):
    if depth == 0 or is_game_over(board):
        return evaluate_board(board, player)
    
    opponent = WHITE if player == BLACK else BLACK
    
    if maximizing_player:
        max_eval = float('-inf')
        valid_moves = get_valid_moves(board, player)
        if not valid_moves:
             return minmax(board, depth-1, False, player, alpha, beta)
             
        for move in valid_moves:
            new_board, _ = apply_move(board, move[0], move[1], player)
            eval = minmax(new_board, depth-1, False, player, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        valid_moves = get_valid_moves(board, opponent)
        if not valid_moves:
            return minmax(board, depth-1, True, player, alpha, beta)
            
        for move in valid_moves:
            new_board, _ = apply_move(board, move[0], move[1], opponent)
            eval = minmax(new_board, depth-1, True, player, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(board, player, depth=3):
    best_move = None
    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    
    valid_moves = get_valid_moves(board, player)
    if not valid_moves:
        return None
        
    for move in valid_moves:
        new_board, _ = apply_move(board, move[0], move[1], player)
        eval = minmax(new_board, depth-1, False, player, alpha, beta)
        if eval > max_eval:
            max_eval = eval
            best_move = move
        alpha = max(alpha, eval)
            
    return best_move
