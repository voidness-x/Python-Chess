import copy
import os
 
 
def create_starting_board():
    return [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        ["0", "0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0", "0"],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ]
 
 
def clear_screen():
    """Clear the terminal so only the current board is ever on screen."""
    os.system("cls" if os.name == "nt" else "clear")
 
 
def print_board(board):
    print("     A  B  C  D  E  F  G  H")
    print("  +==========================+")
    row_label = 8
    for row in board:
        print(row_label, end=" |  ")
        for square in row:
            print(square, end="  ")
        print("|", row_label)
        row_label -= 1
    print("  +==========================+")
    print("     A  B  C  D  E  F  G  H")
 
 
def clone_board(board):
    return copy.deepcopy(board)