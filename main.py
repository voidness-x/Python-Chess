from board import static_board, print_board
from pieces import read_coordinate, piece_check

def main():
    turn = "White"

    while True:
        print_board()
        print (turn, "'s move")
        move = input("|_____ ")

        if move.lower() == 'exit':
            print("Exiting game... Byeeeeeeeeeeeee :3")
            break

        try:
            move = move.replace(" ", "")
            if len(move) != 4:
                print("Error: Input must be exactly 4 characters long (e.g., e2e4 or e2 e4).")
                continue

            start_col = read_coordinate(move)[0]
            start_row = read_coordinate(move)[1]
            end_col   = read_coordinate(move)[2]
            end_row   = read_coordinate(move)[3]

            piece = static_board[start_row][start_col]

            if piece == "0":
                print("Error: There is no piece on the starting square. Try again...")
                continue
            if not piece_check(start_col, start_row, end_col, end_row, piece, turn):
                continue

            static_board[start_row][start_col] = "0"       
            static_board[end_row][end_col] = piece 

            if turn == "White":
                turn = "Black"
            else:
                turn = "White"

        except KeyError:
            print("Error: Invalid files used. Use letters A through H.")
        except ValueError:
            print("Error: Invalid ranks used. Use numbers 1 through 8.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
