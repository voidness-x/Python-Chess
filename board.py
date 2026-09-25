# NOTES:
# Approach: Bitloader (piece orianted) - Postponed
# Check the HW phases
# I hate coding <3
# ♔ ♕ ♖ ♗ ♘ ♙ □
# ♚ ♛ ♜ ♝ ♞ ♟ ■
# [" -- ", "-- ", "-- ", "-- ", "-- ", "-- ", "-- ", "--"],


static_board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]


def print_board():
    print ("     A  B  C  D  E  F  G  H")
    print ("  +==========================+")
    row = 8
    for i in (static_board):
        print (row, end=" |  ")
        for j in i:
            print(j, end="  ")
        print ("|", row)
        row -= 1
    print ("  +==========================+")
    print ("     A  B  C  D  E  F  G  H")


