"""
All user-facing messages for the chess game live here, so every other
module imports them instead of typing its own copies of the strings.
"""

# --- Input parsing errors ---
ERR_BAD_INPUT_LENGTH = ("Input must be exactly 4 characters long (e.g., e2e4 or e2 e4). "
                         "Type 'help' to see other commands.")
ERR_BAD_FILE = "Invalid file used. Files must be letters A through H."
ERR_BAD_RANK = "Invalid rank used. Ranks must be numbers 1 through 8."
ERR_UNEXPECTED = "An unexpected error occurred: {error}"

# --- General move errors ---
ERR_NO_PIECE = "There is no piece on the starting square"
ERR_NOT_YOUR_TURN = "It is {turn}'s turn right now. This is not your piece >~<"
ERR_NO_MOVEMENT = "You have to actually move the piece somewhere >~<"
ERR_FRIENDLY_FIRE = "You cannot capture your own piece :D"
ERR_SELF_CHECK = "That move would leave your own king in check"

# --- Piece-specific movement errors ---
ERR_KNIGHT_SHAPE = "Knights must move in an L-shape"
ERR_KING_RANGE = "Kings can only move 1 square in any direction (unless castling)"
ERR_ROOK_LINE = "Rooks can only move in a straight horizontal or vertical line"
ERR_BISHOP_DIAGONAL = "Bishops can only move diagonally"
ERR_QUEEN_LINE = "Queens must move in a straight line or diagonally"
ERR_BLOCKED_PATH = "There's a piece in the way"
ERR_UNKNOWN_PIECE = "Unknown piece type"

# --- Pawn errors ---
ERR_PAWN_BLOCKED_FORWARD = "Pawns cannot move forward into an occupied square"
ERR_PAWN_BLOCKED_DOUBLE = "The path forward is blocked"
ERR_PAWN_BAD_DISTANCE = "Pawns can only move 1 square forward (or 2 from their starting rank)"
ERR_PAWN_BAD_CAPTURE = "Pawns can only move diagonally when capturing an enemy piece"
ERR_PAWN_INVALID = "Invalid pawn movement trajectory."

# --- Castling errors ---
ERR_CASTLE_RIGHTS_LOST = ("Cannot castle: you no longer have castling rights on that side "
                           "(the king or that rook has already moved, or the rook was captured)")
ERR_CASTLE_ROOK_MOVED = "Cannot castle: there is no rook on that corner square"
ERR_CASTLE_PATH_BLOCKED = "Cannot castle: there are pieces between the king and rook"
ERR_CASTLE_IN_CHECK = "Cannot castle while in check"
ERR_CASTLE_THROUGH_CHECK = "Cannot castle through a square that is under attack"
ERR_CASTLE_INTO_CHECK = "Cannot castle into check"

# --- En passant ---
ERR_EN_PASSANT_UNAVAILABLE = "En passant is not available on that square right now"

# --- Game-flow / command messages ---
MSG_SAVED = "Game saved to {filename} :3"
ERR_SAVE_FAILED = "Could not save game: {error}"
ERR_LOAD_FAILED = "Could not load game: {error}"
MSG_LOADED = "Game loaded from {filename}"
MSG_NOTHING_TO_UNDO = "Nothing to undo yet."
MSG_MOVE_UNDONE = "Move undone."
MSG_NO_HISTORY = "No moves played yet."
MSG_CHECK = "{turn} is in check!"
MSG_CHECKMATE = "Checkmate! {turn} wins! GG :3"
MSG_STALEMATE = "Stalemate -- the game is a draw."
MSG_EXIT = "Exiting game... Byeeeeeeeeeeeee :3"

HELP_TEXT = (
    "Commands:\n"
    "  <move like e2e4>   move a piece from one square to another\n"
    "  O-O / O-O-O        castle kingside / queenside (0-0 also works)\n"
    "  undo               undo the last move\n"
    "  history            show the move history\n"
    "  save [filename]    save the game\n"
    "  load [filename]    load a game\n"
    "  exit               quit\n"
    "(En passant is applied automatically when the position allows it.)"
)