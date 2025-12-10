from colorama import Fore, Style

BOARD_SIZE = 8
EMPTY = 0
BLACK = 1
WHITE = 2

# Colors
BLACK_COLOR = Style.BRIGHT + Fore.BLACK
WHITE_COLOR = Style.BRIGHT + Fore.WHITE
RESET_COLOR = Style.RESET_ALL

# Box Drawing
# Double lines for border
TOP_LEFT = '\u2554'      # ╔
TOP_RIGHT = '\u2557'     # ╗
BOTTOM_LEFT = '\u255a'   # ╚
BOTTOM_RIGHT = '\u255d'  # ╝

BORDER_HORIZONTAL = '\u2550' # ═
BORDER_VERTICAL = '\u2551'   # ║

# Single lines for inner grid
INNER_HORIZONTAL = '\u2500'  # ─
INNER_VERTICAL = '\u2502'    # │

# Mixed junctions (Double border, Single inner)
T_DOWN = '\u2564'   # ╤ (Top edge)
T_UP = '\u2567'     # ╧ (Bottom edge)
T_RIGHT = '\u255f'  # ╟ (Left edge, points right)
T_LEFT = '\u2562'   # ╢ (Right edge, points left)

CROSS = '\u253c'    # ┼ (Inner intersection)

PIECE = '\u2B24'
