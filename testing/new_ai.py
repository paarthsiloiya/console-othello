import time
from constants import BLACK, WHITE, BOARD_SIZE, EMPTY
from game_logic import get_valid_moves, apply_move, is_game_over, get_score
from opening_book import get_opening_move

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

# Bitboard Constants
MASK_A = 0xFEFEFEFEFEFEFEFE
MASK_H = 0x7F7F7F7F7F7F7F7F
FULL_MASK = 0xFFFFFFFFFFFFFFFF

# Precompute Weight Masks
WEIGHT_MASKS = {}
for r in range(8):
    for c in range(8):
        w = WEIGHTS[r][c]
        if w not in WEIGHT_MASKS:
            WEIGHT_MASKS[w] = 0
        WEIGHT_MASKS[w] |= (1 << (r * 8 + c))

TRANSPOSITION_TABLE = {}

def board_to_bitboards(board, player):
    own = 0
    opp = 0
    opponent = WHITE if player == BLACK else BLACK
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p == player:
                own |= (1 << (r * 8 + c))
            elif p == opponent:
                opp |= (1 << (r * 8 + c))
    return own, opp

def get_valid_moves_bitboard(own, opp):
    empty = ~(own | opp) & FULL_MASK
    moves = 0
    
    # East (+1)
    candidates = opp & ((own & MASK_H) << 1)
    while candidates:
        moves |= empty & ((candidates & MASK_H) << 1)
        candidates = opp & ((candidates & MASK_H) << 1)
        
    # West (-1)
    candidates = opp & ((own & MASK_A) >> 1)
    while candidates:
        moves |= empty & ((candidates & MASK_A) >> 1)
        candidates = opp & ((candidates & MASK_A) >> 1)
        
    # South (+8)
    candidates = opp & ((own) << 8)
    while candidates:
        moves |= empty & ((candidates) << 8)
        candidates = opp & ((candidates) << 8)
        
    # North (-8)
    candidates = opp & ((own) >> 8)
    while candidates:
        moves |= empty & ((candidates) >> 8)
        candidates = opp & ((candidates) >> 8)
        
    # SE (+9)
    candidates = opp & ((own & MASK_H) << 9)
    while candidates:
        moves |= empty & ((candidates & MASK_H) << 9)
        candidates = opp & ((candidates & MASK_H) << 9)
        
    # SW (+7)
    candidates = opp & ((own & MASK_A) << 7)
    while candidates:
        moves |= empty & ((candidates & MASK_A) << 7)
        candidates = opp & ((candidates & MASK_A) << 7)
        
    # NE (-7)
    candidates = opp & ((own & MASK_H) >> 7)
    while candidates:
        moves |= empty & ((candidates & MASK_H) >> 7)
        candidates = opp & ((candidates & MASK_H) >> 7)
        
    # NW (-9)
    candidates = opp & ((own & MASK_A) >> 9)
    while candidates:
        moves |= empty & ((candidates & MASK_A) >> 9)
        candidates = opp & ((candidates & MASK_A) >> 9)
        
    return moves

def apply_move_bitboard(own, opp, move_mask):
    flips = 0
    
    # East (+1)
    mask = (move_mask & MASK_H) << 1
    potential = 0
    while mask & opp:
        potential |= mask
        mask = (mask & MASK_H) << 1
    if mask & own: flips |= potential
    
    # West (-1)
    mask = (move_mask & MASK_A) >> 1
    potential = 0
    while mask & opp:
        potential |= mask
        mask = (mask & MASK_A) >> 1
    if mask & own: flips |= potential
    
    # South (+8)
    mask = (move_mask << 8) & FULL_MASK
    potential = 0
    while mask & opp:
        potential |= mask
        mask = (mask << 8) & FULL_MASK
    if mask & own: flips |= potential
    
    # North (-8)
    mask = (move_mask >> 8) & FULL_MASK
    potential = 0
    while mask & opp:
        potential |= mask
        mask = (mask >> 8) & FULL_MASK
    if mask & own: flips |= potential
    
    # SE (+9)
    mask = (move_mask & MASK_H) << 9
    potential = 0
    while mask & opp:
        potential |= mask
        mask = (mask & MASK_H) << 9
    if mask & own: flips |= potential
    
    # SW (+7)
    mask = (move_mask & MASK_A) << 7
    potential = 0
    while mask & opp:
        potential |= mask
        mask = (mask & MASK_A) << 7
    if mask & own: flips |= potential
    
    # NE (-7)
    mask = (move_mask & MASK_H) >> 7
    potential = 0
    while mask & opp:
        potential |= mask
        mask = (mask & MASK_H) >> 7
    if mask & own: flips |= potential
    
    # NW (-9)
    mask = (move_mask & MASK_A) >> 9
    potential = 0
    while mask & opp:
        potential |= mask
        mask = (mask & MASK_A) >> 9
    if mask & own: flips |= potential
    
    return (own | move_mask | flips), (opp & ~flips)

def evaluate_bitboard(own, opp, current_player_is_black):
    # 1. Positional
    my_score = 0
    op_score = 0
    for w, mask in WEIGHT_MASKS.items():
        my_score += w * (own & mask).bit_count()
        op_score += w * (opp & mask).bit_count()
    
    positional_score = my_score - op_score
    
    # 2. Mobility
    my_moves_mask = get_valid_moves_bitboard(own, opp)
    op_moves_mask = get_valid_moves_bitboard(opp, own)
    my_moves_count = my_moves_mask.bit_count()
    op_moves_count = op_moves_mask.bit_count()
    
    if my_moves_count + op_moves_count != 0:
        mobility_score = 100 * (my_moves_count - op_moves_count) / (my_moves_count + op_moves_count)
    else:
        mobility_score = 0
        
    # 3. Coin Parity
    my_coins = own.bit_count()
    op_coins = opp.bit_count()
    
    if my_coins + op_coins != 0:
        coin_parity_score = 100 * (my_coins - op_coins) / (my_coins + op_coins)
    else:
        coin_parity_score = 0
        
    total_coins = my_coins + op_coins
    
    if total_coins < 20:
        return positional_score + 2 * mobility_score
    elif total_coins < 50:
        return positional_score + mobility_score + coin_parity_score
    else:
        return positional_score + 5 * coin_parity_score

def minmax_bitboard(own, opp, depth, maximizing_player, alpha, beta, start_time, time_limit, player_color):
    if time.time() - start_time > time_limit:
        raise TimeoutError
        
    state_key = (own, opp, maximizing_player)
    
    alpha_orig = alpha
    beta_orig = beta
    
    if state_key in TRANSPOSITION_TABLE:
        entry = TRANSPOSITION_TABLE[state_key]
        if entry['depth'] >= depth:
            if entry['flag'] == 'exact':
                return entry['value']
            elif entry['flag'] == 'lowerbound':
                alpha = max(alpha, entry['value'])
            elif entry['flag'] == 'upperbound':
                beta = min(beta, entry['value'])
            if alpha >= beta:
                return entry['value']
                
    if depth == 0:
        return evaluate_bitboard(own, opp, player_color == BLACK)
        
    moves_mask = get_valid_moves_bitboard(own, opp) if maximizing_player else get_valid_moves_bitboard(opp, own)
    
    if moves_mask == 0:
        opp_moves_mask = get_valid_moves_bitboard(opp, own) if maximizing_player else get_valid_moves_bitboard(own, opp)
        if opp_moves_mask == 0:
            return evaluate_bitboard(own, opp, player_color == BLACK)
        else:
            return minmax_bitboard(own, opp, depth-1, not maximizing_player, alpha, beta, start_time, time_limit, player_color)
            
    best_val = float('-inf') if maximizing_player else float('inf')
    
    move_indices = []
    temp_moves = moves_mask
    while temp_moves:
        lsb = temp_moves & -temp_moves
        move_indices.append(lsb)
        temp_moves ^= lsb
        
    def get_weight(move_bit):
        for w, mask in WEIGHT_MASKS.items():
            if mask & move_bit:
                return w
        return 0
        
    move_indices.sort(key=get_weight, reverse=True)
    
    if maximizing_player:
        for move_bit in move_indices:
            new_own, new_opp = apply_move_bitboard(own, opp, move_bit)
            eval = minmax_bitboard(new_own, new_opp, depth-1, False, alpha, beta, start_time, time_limit, player_color)
            best_val = max(best_val, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
    else:
        for move_bit in move_indices:
            new_opp, new_own = apply_move_bitboard(opp, own, move_bit)
            eval = minmax_bitboard(new_own, new_opp, depth-1, True, alpha, beta, start_time, time_limit, player_color)
            best_val = min(best_val, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
                
    if best_val <= alpha_orig:
        flag = 'upperbound'
    elif best_val >= beta_orig:
        flag = 'lowerbound'
    else:
        flag = 'exact'
        
    TRANSPOSITION_TABLE[state_key] = {
        'value': best_val,
        'depth': depth,
        'flag': flag
    }
    return best_val

def get_best_move(board, player, time_limit=2.0):
    # Check Opening Book
    opening_move = get_opening_move(board, player)
    if opening_move:
        return opening_move

    own, opp = board_to_bitboards(board, player)
    
    # Endgame Solver Check
    empty_count = (~(own | opp) & FULL_MASK).bit_count()
    if empty_count <= 12:
        depth = empty_count
        try:
            return get_best_move_fixed_depth_bitboard(own, opp, depth, time_limit * 5, player)
        except TimeoutError:
            pass
            
    start_time = time.time()
    depth = 1
    max_depth = 64
    
    current_best_move = None
    
    try:
        while True:
            if time.time() - start_time > time_limit:
                break
            if depth > max_depth:
                break
                
            move = get_best_move_fixed_depth_bitboard(own, opp, depth, time_limit, player, start_time)
            if move:
                current_best_move = move
                
            depth += 1
            
    except TimeoutError:
        pass
        
    return current_best_move

def get_best_move_fixed_depth_bitboard(own, opp, depth, time_limit, player, start_time=None):
    if start_time is None:
        start_time = time.time()
        
    best_move = None
    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    
    moves_mask = get_valid_moves_bitboard(own, opp)
    if moves_mask == 0:
        return None
        
    move_indices = []
    temp_moves = moves_mask
    while temp_moves:
        lsb = temp_moves & -temp_moves
        move_indices.append(lsb)
        temp_moves ^= lsb
        
    def get_weight(move_bit):
        for w, mask in WEIGHT_MASKS.items():
            if mask & move_bit:
                return w
        return 0
        
    move_indices.sort(key=get_weight, reverse=True)
        
    for move_bit in move_indices:
        new_own, new_opp = apply_move_bitboard(own, opp, move_bit)
        eval = minmax_bitboard(new_own, new_opp, depth-1, False, alpha, beta, start_time, time_limit, player)
        
        if eval > max_eval:
            max_eval = eval
            idx = move_bit.bit_length() - 1
            best_move = (idx // 8, idx % 8)
            
        alpha = max(alpha, eval)
            
    return best_move
