import time
from constants import BLACK, WHITE, BOARD_SIZE, EMPTY
from game_logic import get_valid_moves, apply_move, is_game_over, get_score

# Static weights for the board
WEIGHTS = [
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [10, -2, -1, -1, -1, -1, -2, 10],
    [5, -2, -1, -1, -1, -1, -2, 5],
    [5, -2, -1, -1, -1, -1, -2, 5],
    [10, -2, -1, -1, -1, -1, -2, 10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10, 5, 5, 10, -20, 100]
]

def evaluate_board_improved(board, player):
    opponent = WHITE if player == BLACK else BLACK
    
    my_score = 0
    op_score = 0
    
    # 1. Positional Strategy (Static Weights)
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == player:
                my_score += WEIGHTS[r][c]
            elif board[r][c] == opponent:
                op_score += WEIGHTS[r][c]
    
    positional_score = my_score - op_score
    
    # 2. Mobility (Number of valid moves)
    my_moves = len(get_valid_moves(board, player))
    op_moves = len(get_valid_moves(board, opponent))
    
    if my_moves + op_moves != 0:
        mobility_score = 100 * (my_moves - op_moves) / (my_moves + op_moves)
    else:
        mobility_score = 0
        
    # 3. Coin Parity (Piece count) - More important in endgame
    black_coins, white_coins = get_score(board)
    if player == BLACK:
        my_coins = black_coins
        op_coins = white_coins
    else:
        my_coins = white_coins
        op_coins = black_coins
        
    if my_coins + op_coins != 0:
        coin_parity_score = 100 * (my_coins - op_coins) / (my_coins + op_coins)
    else:
        coin_parity_score = 0
        
    # Dynamic weighting based on game phase
    total_coins = black_coins + white_coins
    
    if total_coins < 20: # Opening
        return positional_score + 2 * mobility_score
    elif total_coins < 50: # Midgame
        return positional_score + mobility_score + coin_parity_score
    else: # Endgame
        return positional_score + 5 * coin_parity_score

def minmax_improved(board, depth, maximizing_player, player, alpha, beta, start_time, time_limit):
    # Check for time limit
    if time.time() - start_time > time_limit:
        raise TimeoutError
        
    if depth == 0 or is_game_over(board):
        return evaluate_board_improved(board, player)
    
    opponent = WHITE if player == BLACK else BLACK
    
    if maximizing_player:
        max_eval = float('-inf')
        valid_moves = get_valid_moves(board, player)
        if not valid_moves:
             return minmax_improved(board, depth-1, False, player, alpha, beta, start_time, time_limit)
             
        # Move ordering: Try corners first? For now, just simple iteration
        for move in valid_moves:
            new_board, _ = apply_move(board, move[0], move[1], player)
            eval = minmax_improved(new_board, depth-1, False, player, alpha, beta, start_time, time_limit)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        valid_moves = get_valid_moves(board, opponent)
        if not valid_moves:
            return minmax_improved(board, depth-1, True, player, alpha, beta, start_time, time_limit)
            
        for move in valid_moves:
            new_board, _ = apply_move(board, move[0], move[1], opponent)
            eval = minmax_improved(new_board, depth-1, True, player, alpha, beta, start_time, time_limit)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(board, player, time_limit=2.0):
    best_move = None
    
    # Endgame Solver Check
    empty_squares = sum(row.count(EMPTY) for row in board)
    if empty_squares <= 10:
        depth = empty_squares # Search to the end
        # print(f"Endgame solver activated (Depth {depth})")
        try:
            return get_best_move_fixed_depth(board, player, depth, time_limit * 5) # Give more time for endgame
        except TimeoutError:
            pass # Fallback to iterative deepening if endgame solve takes too long
            
    # Iterative Deepening
    start_time = time.time()
    depth = 1
    max_depth = 6 # Cap the depth to avoid infinite loops if time limit is loose
    
    current_best_move = None
    
    try:
        while True:
            if time.time() - start_time > time_limit:
                break
            if depth > max_depth:
                break
                
            # print(f"Searching depth {depth}...")
            move = get_best_move_fixed_depth(board, player, depth, time_limit, start_time)
            if move:
                current_best_move = move
                
            depth += 1
            
    except TimeoutError:
        pass
        
    return current_best_move

def get_best_move_fixed_depth(board, player, depth, time_limit, start_time=None):
    if start_time is None:
        start_time = time.time()
        
    best_move = None
    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    
    valid_moves = get_valid_moves(board, player)
    if not valid_moves:
        return None
        
    # Simple move ordering: prioritize corners
    corners = [(0, 0), (0, BOARD_SIZE-1), (BOARD_SIZE-1, 0), (BOARD_SIZE-1, BOARD_SIZE-1)]
    valid_moves.sort(key=lambda m: m in corners, reverse=True)
        
    for move in valid_moves:
        new_board, _ = apply_move(board, move[0], move[1], player)
        eval = minmax_improved(new_board, depth-1, False, player, alpha, beta, start_time, time_limit)
        if eval > max_eval:
            max_eval = eval
            best_move = move
        alpha = max(alpha, eval)
            
    return best_move
