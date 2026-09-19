# filename: tictactoe.py

def print_board(board):
    print('---------')
    for row in board:
        print('|', end='')
        for cell in row:
            print(cell or ' ', end=' ')
        print('|')
    print('---------')

def win(board, player):
    win_states = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]
    return any(state.count(player) == 3 for state in win_states)

def full(board):
    return all(cell != None for row in board for cell in row)

board = [[None, None, None] for _ in range(3)]
players = ['X', 'O']
current_player = 0

while True:
    print_board(board)
    row = int(input(f'Player {players[current_player]}, enter row: '))
    col = int(input(f'Player {players[current_player]}, enter column: '))
    if board[row - 1][col - 1] is not None:
        print("This cell is already chosen. Try again")
        continue
    board[row - 1][col - 1] = players[current_player]
    if win(board, players[current_player]):
        print(f'Player {players[current_player]} wins!')
        if input('Play again? (yes/no): ').lower() == 'no':
            break
        board = [[None, None, None] for _ in range(3)]
    elif full(board):
        print('Draw!')
        if input('Play again? (yes/no): ').lower() == 'no':
            break
        board = [[None, None, None] for _ in range(3)]
    else:
        current_player = 1 - current_player