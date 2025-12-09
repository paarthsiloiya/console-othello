from game_logic import create_board, apply_move
from constants import BLACK, WHITE, BOARD_SIZE

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

class OpeningBook:
    def __init__(self):
        self.book = {}
        self._initialize_book()

    def _add_sequence(self, moves):
        board = create_board()
        player = BLACK
        
        for r, c in moves:
            own, opp = board_to_bitboards(board, player)
            
            if (own, opp) not in self.book:
                self.book[(own, opp)] = (r, c)
            
            board, _ = apply_move(board, r, c, player)
            player = WHITE if player == BLACK else BLACK

    def _initialize_book(self):
        self._add_sequence([(4, 5), (5, 3), (2, 2), (2, 3), (3, 2), (3, 5)])
        self._add_sequence([(4, 5), (5, 5), (5, 4), (3, 5), (2, 4)])
        self._add_sequence([(4, 5), (5, 3), (3, 2), (2, 3)])
        self._add_sequence([(2, 3), (4, 2), (5, 3)])
        self._add_sequence([(3, 2), (2, 4), (4, 5)])
        self._add_sequence([(5, 4), (3, 5), (4, 2)])

    def get_move(self, board, player):
        own, opp = board_to_bitboards(board, player)
        return self.book.get((own, opp))

_book_instance = OpeningBook()

def get_opening_move(board, player):
    return _book_instance.get_move(board, player)
