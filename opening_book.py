from game_logic import create_board, apply_move
from constants import BLACK, WHITE, BOARD_SIZE

def board_to_bitboards(board, player):
    """
    Converts the board to bitboards for the opening book key generation.

    Args:
        board (list): The 2D list representation of the board.
        player (str): The current player's color.

    Returns:
        tuple: A tuple (own, opp) of bitboards.
    """
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
    """
    Manages the opening book for the Othello AI.
    
    Stores a collection of pre-calculated opening sequences to allow the AI
    to play instantly and optimally during the early game.
    """
    def __init__(self):
        """Initialize the OpeningBook and load sequences."""
        self.book = {}
        self._initialize_book()

    def _add_sequence(self, moves):
        """
        Adds a sequence of moves to the opening book.

        Args:
            moves (list): A list of (row, col) tuples representing the move sequence.
        """
        board = create_board()
        player = BLACK
        
        for r, c in moves:
            own, opp = board_to_bitboards(board, player)
            
            if (own, opp) not in self.book:
                self.book[(own, opp)] = (r, c)
            
            board, _ = apply_move(board, r, c, player)
            player = WHITE if player == BLACK else BLACK

    def _initialize_book(self):
        """
        Populates the book with standard Othello opening lines.
        """
        self._add_sequence([(4, 5), (5, 3), (2, 2), (2, 3), (3, 2), (3, 5)])
        self._add_sequence([(4, 5), (5, 5), (5, 4), (3, 5), (2, 4)])
        self._add_sequence([(4, 5), (5, 3), (3, 2), (2, 3)])
        self._add_sequence([(2, 3), (4, 2), (5, 3)])
        self._add_sequence([(3, 2), (2, 4), (4, 5)])
        self._add_sequence([(5, 4), (3, 5), (4, 2)])

    def get_move(self, board, player):
        """
        Retrieves a move from the opening book if the current board state exists in it.

        Args:
            board (list): The current game board.
            player (str): The current player.

        Returns:
            tuple or None: The (row, col) of the move, or None if not found.
        """
        own, opp = board_to_bitboards(board, player)
        return self.book.get((own, opp))

_book_instance = OpeningBook()

def get_opening_move(board, player):
    """
    Public interface to get a move from the opening book.

    Args:
        board (list): The current game board.
        player (str): The current player.

    Returns:
        tuple or None: The (row, col) of the move, or None if not found.
    """
    return _book_instance.get_move(board, player)
