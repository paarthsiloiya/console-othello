import os
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
