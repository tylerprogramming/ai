def print_board(board):
    """Function to print the current state of the board."""
    for row in board:
        print("|".join(row))
    print("-" * 5)


def check_winner(board):
    """Function to check if there's a winner."""
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return True
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return True
        if board[0][0] == board[1][1] == board[2][2] != " ":
            return True
        if board[0][2] == board[1][1] == board[2][0] != " ":
            return True
    return False


def tic_tac_toe():
    """Main function to play Tic-Tac-Toe."""
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    moves = 0
    while moves < 9:
        print_board(board)
        row = int(input(f"Player {current_player}, enter the row (0, 1, or 2): "))
        col = int(input(f"Player {current_player}, enter the column (0, 1, or 2): "))
        if board[row][col] == " ":
            board[row][col] = current_player
            moves += 1
            if check_winner(board):
                print_board(board)
                print(f"Player {current_player} wins!")
                return
            current_player = "O" if current_player == "X" else "X"
        else:
            print("Position already taken, try again!")
    print_board(board)
    print("It's a draw!")


tic_tac_toe()
