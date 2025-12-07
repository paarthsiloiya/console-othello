import os
import time
import bext
from colorama import init, Fore, Style
from constants import *

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    header = "    " + "   ".join([chr(ord('A') + i) for i in range(BOARD_SIZE)])
    print(header)
    
    top_border = "  " + TOP_LEFT + (HORIZONTAL * 3 + T_DOWN) * (BOARD_SIZE - 1) + HORIZONTAL * 3 + TOP_RIGHT
    print(top_border)
    
    for r in range(BOARD_SIZE):
        line = f"{r+1} {VERTICAL}"
        for c in range(BOARD_SIZE):
            piece = board[r][c]
            if piece == BLACK:
                symbol = Fore.RED + PIECE + Style.RESET_ALL
            elif piece == WHITE:
                symbol = Fore.CYAN + PIECE + Style.RESET_ALL
            else:
                symbol = " "
            line += f" {symbol} {VERTICAL}"
        print(line)
        
        if r < BOARD_SIZE - 1:
            mid_border = "  " + T_RIGHT + (HORIZONTAL * 3 + CROSS) * (BOARD_SIZE - 1) + HORIZONTAL * 3 + T_LEFT
            print(mid_border)
            
    bottom_border = "  " + BOTTOM_LEFT + (HORIZONTAL * 3 + T_UP) * (BOARD_SIZE - 1) + HORIZONTAL * 3 + BOTTOM_RIGHT
    print(bottom_border)

def print_score(black_score, white_score):
    print(f"{Fore.RED}Black: {black_score}{Style.RESET_ALL}  {Fore.CYAN}White: {white_score}{Style.RESET_ALL}")

def print_welcome():
    clear_screen()
    print(Fore.YELLOW + Style.BRIGHT + r"""
   ____  _   _          _ _       
  / __ \| | | |        | | |      
 | |  | | |_| |__   ___| | | ___  
 | |  | | __| '_ \ / _ \ | |/ _ \ 
 | |__| | |_| | | |  __/ | | (_) |
  \____/ \__|_| |_|\___|_|_|\___/ 
                                  
""" + Style.RESET_ALL)
    print(f"{Style.BRIGHT}Welcome to Console Othello!{Style.RESET_ALL}")
    print("Rules: Capture opponent's pieces by trapping them between yours.")
    print(f"Player 1 ({Fore.RED}{PIECE}{Style.RESET_ALL}) vs Player 2 ({Fore.CYAN}{PIECE}{Style.RESET_ALL})")
    print()

def print_message(msg):
    print(msg)

def animate_flip(flipped_groups, player, placed_pos=None):
    bext.hide_cursor()
    if placed_pos:
        r, c = placed_pos
        x = 4 + 4 * c
        y = 2 + 2 * r
        if player == BLACK:
            color = Fore.RED
        else:
            color = Fore.CYAN
        try:
            bext.goto(x, y)
            print(color + PIECE + Style.RESET_ALL, end='', flush=True)
        except:
            pass

    if not flipped_groups:
        return

    max_len = 0
    for group in flipped_groups:
        if len(group) > max_len:
            max_len = len(group)
            
    final_char = PIECE
    
    if player == BLACK:
        final_color = Fore.RED
    else:
        final_color = Fore.CYAN
        
    middle_color = final_color
    
    # Determine characters for each group
    group_chars = []
    if placed_pos:
        pr, pc = placed_pos
        for group in flipped_groups:
            if not group:
                group_chars.append('/')
                continue
            fr, fc = group[0]
            dr = fr - pr
            dc = fc - pc
            
            if dr == 0: # Horizontal
                char = '|'
            elif dc == 0: # Vertical
                char = '|'
            elif (dr > 0 and dc > 0) or (dr < 0 and dc < 0): # Main diagonal (\)
                char = '\\'
            else: # Anti-diagonal (/)
                char = '/'
            group_chars.append(char)
    else:
        group_chars = ['/'] * len(flipped_groups)
    
    for step in range(max_len + 2):
        for i, group in enumerate(flipped_groups):
            middle_char = group_chars[i]
            
            # Middle state
            if step < len(group):
                r, c = group[step]
                x = 4 + 4 * c
                y = 2 + 2 * r
                try:
                    bext.goto(x, y)
                    print(middle_color + middle_char + Style.RESET_ALL, end='', flush=True)
                except:
                    pass
                
            # Final state
            if step - 1 >= 0 and step - 1 < len(group):
                r, c = group[step - 1]
                x = 4 + 4 * c
                y = 2 + 2 * r
                try:
                    bext.goto(x, y)
                    print(final_color + final_char + Style.RESET_ALL, end='', flush=True)
                except:
                    pass
                
        time.sleep(0.2)
        
    try:
        bext.goto(0, 2 + 2 * BOARD_SIZE + 2)
    except:
        pass
    
    bext.show_cursor()
