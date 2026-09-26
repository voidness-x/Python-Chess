from board import clone_board
from errors import (
    ERR_NO_MOVEMENT, ERR_FRIENDLY_FIRE, ERR_KNIGHT_SHAPE, ERR_KING_RANGE,
    ERR_ROOK_LINE, ERR_BISHOP_DIAGONAL, ERR_QUEEN_LINE, ERR_BLOCKED_PATH,
    ERR_UNKNOWN_PIECE, ERR_PAWN_BLOCKED_FORWARD, ERR_PAWN_BLOCKED_DOUBLE,
    ERR_PAWN_BAD_DISTANCE, ERR_PAWN_BAD_CAPTURE, ERR_PAWN_INVALID,
    ERR_NO_PIECE, ERR_NOT_YOUR_TURN, ERR_SELF_CHECK,
    ERR_CASTLE_RIGHTS_LOST, ERR_CASTLE_ROOK_MOVED, ERR_CASTLE_PATH_BLOCKED,
    ERR_CASTLE_IN_CHECK, ERR_CASTLE_THROUGH_CHECK, ERR_CASTLE_INTO_CHECK,
    ERR_EN_PASSANT_UNAVAILABLE,
)

FILES = "ABCDEFGH"
file_col = {f: i for i, f in enumerate(FILES)}
col_file = {i: f.lower() for i, f in enumerate(FILES)}


def default_castling_rights():
    return {"White": {"K": True, "Q": True}, "Black": {"K": True, "Q": True}}


def read_coordinate(coord):
    """Parses a 4-character move like 'e2e4' into board (row, col) indices.

    Raises KeyError for an invalid file letter, ValueError for an invalid
    or out-of-range rank digit -- callers rely on catching those.
    """
    coord = coord.upper()
    start_col = file_col[coord[0]]
    end_col = file_col[coord[2]]
    start_rank = int(coord[1])
    end_rank = int(coord[3])
    if not (1 <= start_rank <= 8) or not (1 <= end_rank <= 8):
        raise ValueError("Rank must be between 1 and 8")
    start_row = 8 - start_rank
    end_row = 8 - end_rank
    return start_row, start_col, end_row, end_col


def square_name(row, col):
    return col_file[col] + str(8 - row)


def color_check(board, row, col):
    piece = board[row][col]
    if piece == "0":
        return None
    elif piece.isupper():
        return "White"
    else:
        return "Black"


def _sign(x):
    return (x > 0) - (x < 0)


def path_check(board, start_row, start_col, end_row, end_col):
    """True if every square strictly between start and end is empty."""
    row_step = _sign(end_row - start_row)
    col_step = _sign(end_col - start_col)

    row, col = start_row + row_step, start_col + col_step
    while (row, col) != (end_row, end_col):
        if board[row][col] != "0":
            return False
        row += row_step
        col += col_step

    return True


def can_piece_reach(board, start_row, start_col, end_row, end_col):
    """Pure movement-pattern legality for the piece at the start square.

    Does NOT consider whose turn it is -- only whether the piece could
    physically make that move on this board (shape, blocking pieces, and
    not landing on a friendly piece). This makes it safe to reuse both for
    validating the player's move and for figuring out which squares a
    piece attacks (used for check detection).
    """
    piece = board[start_row][start_col]
    piece_type = piece.lower()
    piece_color = color_check(board, start_row, start_col)
    target_color = color_check(board, end_row, end_col)

    col_diff = abs(end_col - start_col)
    row_diff = abs(end_row - start_row)

    if (start_row, start_col) == (end_row, end_col):
        return False, ERR_NO_MOVEMENT

    if target_color == piece_color:
        return False, ERR_FRIENDLY_FIRE

    if piece_type == 'n':
        if col_diff * row_diff == 2:
            return True, ""
        return False, ERR_KNIGHT_SHAPE

    elif piece_type == 'k':
        if max(col_diff, row_diff) == 1:
            return True, ""
        return False, ERR_KING_RANGE

    elif piece_type == 'r':
        if col_diff != 0 and row_diff != 0:
            return False, ERR_ROOK_LINE
        if not path_check(board, start_row, start_col, end_row, end_col):
            return False, ERR_BLOCKED_PATH
        return True, ""

    elif piece_type == 'b':
        if col_diff != row_diff:
            return False, ERR_BISHOP_DIAGONAL
        if not path_check(board, start_row, start_col, end_row, end_col):
            return False, ERR_BLOCKED_PATH
        return True, ""

    elif piece_type == 'q':
        is_straight = (col_diff == 0 or row_diff == 0)
        is_diagonal = (col_diff == row_diff)
        if not (is_straight or is_diagonal):
            return False, ERR_QUEEN_LINE
        if not path_check(board, start_row, start_col, end_row, end_col):
            return False, ERR_BLOCKED_PATH
        return True, ""

    elif piece_type == 'p':
        return pawn_check(board, start_row, start_col, end_row, end_col, piece_color)

    else:
        return False, ERR_UNKNOWN_PIECE


def pawn_check(board, start_row, start_col, end_row, end_col, piece_color):
    col_diff = abs(end_col - start_col)
    row_diff = end_row - start_row

    forward = -1 if piece_color == "White" else 1
    starting_row = 6 if piece_color == "White" else 1

    is_target_empty = board[end_row][end_col] == "0"

    if col_diff == 0:
        if row_diff == forward:
            if not is_target_empty:
                return False, ERR_PAWN_BLOCKED_FORWARD
            return True, ""
        elif row_diff == 2 * forward and start_row == starting_row:
            middle_row = start_row + forward
            if board[middle_row][start_col] != "0" or not is_target_empty:
                return False, ERR_PAWN_BLOCKED_DOUBLE
            return True, ""
        else:
            return False, ERR_PAWN_BAD_DISTANCE

    elif col_diff == 1 and row_diff == forward:
        if is_target_empty:
            return False, ERR_PAWN_BAD_CAPTURE
        return True, ""

    return False, ERR_PAWN_INVALID


def find_king(board, color):
    target = 'K' if color == "White" else 'k'
    for row in range(8):
        for col in range(8):
            if board[row][col] == target:
                return row, col
    return None


def is_square_attacked(board, row, col, by_color):
    for r in range(8):
        for c in range(8):
            if color_check(board, r, c) != by_color:
                continue
            ok, _ = can_piece_reach(board, r, c, row, col)
            if ok:
                return True
    return False


def is_in_check(board, color):
    king_pos = find_king(board, color)
    if king_pos is None:
        return False
    opponent = "Black" if color == "White" else "White"
    return is_square_attacked(board, king_pos[0], king_pos[1], opponent)


def simulate_move(board, start_row, start_col, end_row, end_col):
    new_board = clone_board(board)
    new_board[end_row][end_col] = new_board[start_row][start_col]
    new_board[start_row][start_col] = "0"
    return new_board


def simulate_en_passant(board, start_row, start_col, end_row, end_col, captured_row):
    new_board = clone_board(board)
    new_board[end_row][end_col] = new_board[start_row][start_col]
    new_board[start_row][start_col] = "0"
    new_board[captured_row][end_col] = "0"
    return new_board


def is_legal_castle(board, turn, start_col, end_col, castling_rights):
    row = 7 if turn == "White" else 0
    king_side = end_col > start_col
    side_key = "K" if king_side else "Q"

    rights = (castling_rights or {}).get(turn, {})
    if not rights.get(side_key, False):
        return False, ERR_CASTLE_RIGHTS_LOST

    rook_col = 7 if king_side else 0
    expected_rook = 'R' if turn == "White" else 'r'
    if board[row][rook_col] != expected_rook:
        return False, ERR_CASTLE_ROOK_MOVED

    step = 1 if king_side else -1
    col = 4 + step
    while col != rook_col:
        if board[row][col] != "0":
            return False, ERR_CASTLE_PATH_BLOCKED
        col += step

    opponent = "Black" if turn == "White" else "White"
    if is_square_attacked(board, row, 4, opponent):
        return False, ERR_CASTLE_IN_CHECK

    pass_col = 4 + step
    land_col = 4 + 2 * step
    if is_square_attacked(board, row, pass_col, opponent):
        return False, ERR_CASTLE_THROUGH_CHECK
    if is_square_attacked(board, row, land_col, opponent):
        return False, ERR_CASTLE_INTO_CHECK

    return True, ""


def apply_castle(board, turn, end_col):
    """Relocates the rook after the king itself has already been moved."""
    row = 7 if turn == "White" else 0
    king_side = end_col > 4
    rook_from = 7 if king_side else 0
    rook_to = 5 if king_side else 3
    rook_piece = board[row][rook_from]
    board[row][rook_from] = "0"
    board[row][rook_to] = rook_piece


def update_castling_rights(castling_rights, piece, start_row, start_col, end_row, end_col, turn):
    if piece.lower() == 'k':
        castling_rights[turn]["K"] = False
        castling_rights[turn]["Q"] = False

    if piece.lower() == 'r':
        home_row = 7 if turn == "White" else 0
        if start_row == home_row and start_col == 0:
            castling_rights[turn]["Q"] = False
        elif start_row == home_row and start_col == 7:
            castling_rights[turn]["K"] = False

    opponent = "Black" if turn == "White" else "White"
    opp_home_row = 7 if opponent == "White" else 0
    if end_row == opp_home_row and end_col == 0:
        castling_rights[opponent]["Q"] = False
    elif end_row == opp_home_row and end_col == 7:
        castling_rights[opponent]["K"] = False


def is_legal_move(board, start_row, start_col, end_row, end_col, turn,
                   castling_rights=None, en_passant_target=None):
    piece = board[start_row][start_col]
    if piece == "0":
        return False, ERR_NO_PIECE

    piece_color = color_check(board, start_row, start_col)
    if piece_color != turn:
        return False, ERR_NOT_YOUR_TURN.format(turn=turn)

    is_castle_attempt = (piece.lower() == 'k' and start_row == end_row
                          and abs(end_col - start_col) == 2)

    forward = -1 if turn == "White" else 1
    is_ep_attempt = (piece.lower() == 'p' and en_passant_target is not None
                      and (end_row, end_col) == en_passant_target
                      and abs(end_col - start_col) == 1
                      and (end_row - start_row) == forward)

    if is_castle_attempt:
        return is_legal_castle(board, turn, start_col, end_col, castling_rights)

    if is_ep_attempt:
        captured_row = start_row
        if board[captured_row][end_col].lower() != 'p' or color_check(board, captured_row, end_col) == turn:
            return False, ERR_EN_PASSANT_UNAVAILABLE
        hypothetical = simulate_en_passant(board, start_row, start_col, end_row, end_col, captured_row)
    else:
        ok, reason = can_piece_reach(board, start_row, start_col, end_row, end_col)
        if not ok:
            return False, reason
        hypothetical = simulate_move(board, start_row, start_col, end_row, end_col)

    if is_in_check(hypothetical, turn):
        return False, ERR_SELF_CHECK

    return True, ""


def has_any_legal_move(board, color, castling_rights=None, en_passant_target=None):
    for start_row in range(8):
        for start_col in range(8):
            if color_check(board, start_row, start_col) != color:
                continue
            for end_row in range(8):
                for end_col in range(8):
                    ok, _ = is_legal_move(board, start_row, start_col, end_row, end_col, color,
                                           castling_rights, en_passant_target)
                    if ok:
                        return True
    return False


def is_checkmate(board, color, castling_rights=None, en_passant_target=None):
    return (is_in_check(board, color)
            and not has_any_legal_move(board, color, castling_rights, en_passant_target))


def is_stalemate(board, color, castling_rights=None, en_passant_target=None):
    return (not is_in_check(board, color)
            and not has_any_legal_move(board, color, castling_rights, en_passant_target))


def move_to_notation(piece, start_row, start_col, end_row, end_col,
                      is_capture, promotion=None, gives_check=False, gives_mate=False,
                      is_castle_kingside=False, is_castle_queenside=False, is_en_passant=False):
    if is_castle_kingside:
        notation = "O-O"
    elif is_castle_queenside:
        notation = "O-O-O"
    else:
        piece_type = piece.upper()
        dest = square_name(end_row, end_col)

        if piece_type == 'P':
            if is_capture:
                origin_file = col_file[start_col]
                notation = f"{origin_file}x{dest}"
            else:
                notation = dest
            if promotion:
                notation += f"={promotion.upper()}"
            if is_en_passant:
                notation += " e.p."
        else:
            notation = piece_type + ("x" if is_capture else "") + dest

    if gives_mate:
        notation += "#"
    elif gives_check:
        notation += "+"

    return notation