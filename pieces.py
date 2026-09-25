from board import static_board

file_col = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}

def read_coordinate(coord):

    coord = coord.upper()
    start_col = file_col[coord[0]]
    start_row = 8 - int(coord[1])
    end_col   = file_col[coord[2]]
    end_row   = 8 - int(coord[3])

    return start_col, start_row, end_col, end_row


def empty_check(col, row):

    if static_board[row][col] != "0":
        print("The square is already taken by another piece :p")
        return False
    
    return True       # Need to check if this works later on


def color_check(col, row):

    piece = static_board[row][col]

    if piece == "0":
        return None
    elif piece.isupper():
        return "White"
    else:
        return "Black"


def path_check(start_col, start_row, end_col, end_row):

    if end_col > start_col:
        col_step = 1
    elif end_col < start_col:
        col_step = -1
    else:
        col_step = 0
    
    if end_row > start_row:
        row_step = 1
    elif end_row < start_row:
        row_step = -1
    else:
        row_step = 0

    col = start_col + col_step
    row = start_row + row_step

    while (col, row) != (end_col, end_row):

        if not empty_check(col, row):
            return False
        
        col += col_step
        row += row_step
 
    return True


def piece_check(start_col, start_row, end_col, end_row, piece_type, turn):

    col = abs(end_col - start_col)
    row = abs(end_row - start_row)
    piece = piece_type.lower()

    piece_color = color_check(start_col, start_row)
    target_color = color_check(end_col, end_row)

    if piece_color != turn:
        print ("it is ", turn,"'s turn now. This is not your piece >~<")
        return False

    if target_color == turn:
        print ("You cannot capture your own piece :D ")
        return False

    if piece == 'n':  
        if (col * row) == 2:
            return True
        else:
            print ("Knights must move in L-shape")
            return False

    elif piece == 'k':
        if max(col, row) == 1:
            return True
        else:
            print ("Kings can only move 1 square in any direction ")
            return False

    elif piece == 'r':
        if col != 0 and row != 0:
            print ("Rooks can only move straight horizontally or vertically")
            return False
        
    elif piece == 'b':
        if col != row:
            print ("Bishops can only move diagonally")
            return False
            
    elif piece == 'q':
        is_straight = (col == 0 or row == 0)
        is_diagonal = (col == row)
        if not (is_straight or is_diagonal):
            print ("Queens must move straight or diagonally.")
            return False

    elif piece == 'p':
        return pawn_check(start_col, start_row, end_col, end_row, piece_color)

    else:
        return False

    return path_check(start_col, start_row, end_col, end_row)


def pawn_check (start_col, start_row, end_col, end_row, piece_color):

    col = abs(end_col - start_col)
    row = end_row - start_row           # no abs for one way direction

    if piece_color == "White":
        forward_direction = -1
    else:
        forward_direction = 1

    if piece_color == "White":
        starting_row = 6
    else:
        starting_row = 1

    is_target_empty = empty_check(end_col, end_row)

    if col == 0:
        if row == forward_direction:
            if not is_target_empty:
                print ("Pawns cannot move forward into an occupied square")
                return False
            return True
            
        elif row == (2 * forward_direction) and start_row == starting_row:
            middle_row = start_row + forward_direction
            if not is_target_empty or not empty_check(start_col, middle_row):
                print ("The path forward is blocked")
                return False
            return True
            
        else:
            print ("Pawns can only move 1 square forward (or 2 from their starting rank)")
            return False

    elif col == 1 and row == forward_direction:
        if is_target_empty:
            print ("Pawns can only move diagonally when capturing an enemy piece")
            return False
        return True, ""

    return False, "Invalid pawn movement trajectory."



