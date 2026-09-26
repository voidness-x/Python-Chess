import copy
import json
 
from board import create_starting_board, print_board, clone_board, clear_screen
from pieces import (
    read_coordinate, is_legal_move, is_in_check, is_checkmate, is_stalemate,
    move_to_notation, apply_castle, update_castling_rights, default_castling_rights,
)
from errors import (
    ERR_BAD_INPUT_LENGTH, ERR_BAD_FILE, ERR_BAD_RANK, ERR_UNEXPECTED,
    MSG_SAVED, ERR_SAVE_FAILED, ERR_LOAD_FAILED, MSG_LOADED,
    MSG_NOTHING_TO_UNDO, MSG_MOVE_UNDONE, MSG_NO_HISTORY,
    MSG_CHECK, MSG_CHECKMATE, MSG_STALEMATE, MSG_EXIT, HELP_TEXT,
)
 
DEFAULT_SAVE_FILE = "chess_save.json"
 
 
def format_history(history):
    lines = []
    for i in range(0, len(history), 2):
        move_no = i // 2 + 1
        white_move = history[i]
        black_move = history[i + 1] if i + 1 < len(history) else ""
        lines.append(f"{move_no}. {white_move}  {black_move}".rstrip())
    return lines
 
 
def save_game(board, turn, history, castling_rights, en_passant_target, filename):
    data = {
        "board": board,
        "turn": turn,
        "history": history,
        "castling_rights": castling_rights,
        "en_passant_target": list(en_passant_target) if en_passant_target else None,
    }
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        return MSG_SAVED.format(filename=filename)
    except OSError as e:
        return ERR_SAVE_FAILED.format(error=e)
 
 
def load_game(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        board = data["board"]
        turn = data["turn"]
        history = data["history"]
        castling_rights = data.get("castling_rights", default_castling_rights())
        ep = data.get("en_passant_target")
        en_passant_target = tuple(ep) if ep else None
        return board, turn, history, castling_rights, en_passant_target, None
    except (OSError, json.JSONDecodeError, KeyError) as e:
        return None, None, None, None, None, ERR_LOAD_FAILED.format(error=e)
 
 
def prompt_promotion():
    valid = {"Q", "R", "B", "N"}
    while True:
        choice = input("Promote pawn to [Q/R/B/N]: ").strip().upper()
        if choice in valid:
            return choice
        print("Please choose Q, R, B, or N.")
 
 
def main():
    board = create_starting_board()
    turn = "White"
    move_history = []
    undo_stack = []
    castling_rights = default_castling_rights()
    en_passant_target = None
    status_message = None
 
    while True:
        clear_screen()
        print_board(board)
 
        if move_history:
            print(f"Last move: {move_history[-1]}")
        if status_message:
            print(status_message)
        status_message = None
 
        print(f"{turn}'s move  (type 'help' for commands)")
        raw = input("|_____ ").strip()
        command = raw.lower()
 
        if command == 'exit':
            clear_screen()
            print_board(board)
            print(MSG_EXIT)
            break
 
        if command == 'help':
            status_message = HELP_TEXT
            continue
 
        if command == 'history':
            if not move_history:
                status_message = MSG_NO_HISTORY
            else:
                status_message = "Move history:\n" + "\n".join(
                    "    " + line for line in format_history(move_history)
                )
            continue
 
        if command == 'undo':
            if not undo_stack:
                status_message = MSG_NOTHING_TO_UNDO
            else:
                board, turn, hist_len, castling_rights, en_passant_target = undo_stack.pop()
                move_history = move_history[:hist_len]
                status_message = MSG_MOVE_UNDONE
            continue
 
        parts = raw.split()
        if parts and parts[0].lower() == 'save':
            filename = parts[1] if len(parts) > 1 else DEFAULT_SAVE_FILE
            status_message = save_game(board, turn, move_history, castling_rights,
                                        en_passant_target, filename)
            continue
 
        if parts and parts[0].lower() == 'load':
            filename = parts[1] if len(parts) > 1 else DEFAULT_SAVE_FILE
            new_board, new_turn, new_history, new_rights, new_ep, error = load_game(filename)
            if error:
                status_message = error
            else:
                board, turn, move_history = new_board, new_turn, new_history
                castling_rights, en_passant_target = new_rights, new_ep
                undo_stack = []
                status_message = MSG_LOADED.format(filename=filename)
            continue
 
        # Castling shorthand: O-O / O-O-O (or 0-0 / 0-0-0)
        if command in ('o-o', '0-0'):
            raw = "e1g1" if turn == "White" else "e8g8"
        elif command in ('o-o-o', '0-0-0'):
            raw = "e1c1" if turn == "White" else "e8c8"
 
        move = raw.replace(" ", "")
 
        try:
            if len(move) != 4:
                status_message = f"Error: {ERR_BAD_INPUT_LENGTH}"
                continue
 
            start_row, start_col, end_row, end_col = read_coordinate(move)
            piece = board[start_row][start_col]
 
            legal, error_message = is_legal_move(board, start_row, start_col, end_row, end_col,
                                                  turn, castling_rights, en_passant_target)
            if not legal:
                status_message = f"Error: {error_message}"
                continue
 
            is_castle = (piece.lower() == 'k' and start_row == end_row
                         and abs(end_col - start_col) == 2)
            is_en_passant = (piece.lower() == 'p' and en_passant_target == (end_row, end_col)
                              and board[end_row][end_col] == "0")
 
            # Snapshot for undo BEFORE mutating anything
            undo_stack.append((clone_board(board), turn, len(move_history),
                                copy.deepcopy(castling_rights), en_passant_target))
 
            is_capture = board[end_row][end_col] != "0" or is_en_passant
 
            if is_en_passant:
                board[start_row][end_col] = "0"
 
            board[start_row][start_col] = "0"
            board[end_row][end_col] = piece
 
            if is_castle:
                apply_castle(board, turn, end_col)
 
            promotion = None
            if piece.lower() == 'p' and end_row in (0, 7):
                promotion = prompt_promotion()
                board[end_row][end_col] = promotion if turn == "White" else promotion.lower()
 
            update_castling_rights(castling_rights, piece, start_row, start_col,
                                    end_row, end_col, turn)
 
            new_en_passant_target = None
            if piece.lower() == 'p' and abs(end_row - start_row) == 2:
                new_en_passant_target = ((start_row + end_row) // 2, start_col)
            en_passant_target = new_en_passant_target
 
            next_turn = "Black" if turn == "White" else "White"
            gives_check = is_in_check(board, next_turn)
            gives_mate = gives_check and is_checkmate(board, next_turn, castling_rights,
                                                       en_passant_target)
 
            is_castle_kingside = is_castle and end_col > start_col
            is_castle_queenside = is_castle and end_col < start_col
 
            notation = move_to_notation(piece, start_row, start_col, end_row, end_col,
                                         is_capture, promotion, gives_check, gives_mate,
                                         is_castle_kingside, is_castle_queenside, is_en_passant)
            move_history.append(notation)
 
            if gives_mate:
                clear_screen()
                print_board(board)
                print(f"Last move: {move_history[-1]}")
                print(MSG_CHECKMATE.format(turn=turn))
                break
 
            if is_stalemate(board, next_turn, castling_rights, en_passant_target):
                clear_screen()
                print_board(board)
                print(f"Last move: {move_history[-1]}")
                print(MSG_STALEMATE)
                break
 
            turn = next_turn
            if gives_check:
                status_message = MSG_CHECK.format(turn=turn)
 
        except KeyError:
            status_message = f"Error: {ERR_BAD_FILE}"
        except ValueError:
            status_message = f"Error: {ERR_BAD_RANK}"
        except Exception as e:
            status_message = f"Error: {ERR_UNEXPECTED.format(error=e)}"
 
 
if __name__ == "__main__":
    main()