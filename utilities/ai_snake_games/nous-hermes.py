def print_board(snake):
    board = [['.' for _ in range(20)] for _ in range(20)]  # Define board here
    for row in range(-10, 11):
        for col in range(-10, 11):
            if (row, col) in snake:
                board[row][col] = "S"
            else:
                board[row][col] = "."
    for row in board:
        print(" ".join(row))
    print()

def move_snake(snake, direction):
    head = snake[-1]
    new_tail = (head[0], head[1])
    if direction == 'up':
        new_head = (head[0] - 1, head[1])
    elif direction == 'down':
        new_head = (head[0] + 1, head[1])
    elif direction == 'left':
        new_head = (head[0], head[1] - 1)
    elif direction == 'right':
        new_head = (head[0], head[1] + 1)

    return [new_head] + snake[:-1] + [new_tail]

def main():
    board = [[["." for _ in range(20)] for _ in range(20)]] # Define board here
    snake = [(9, 9), (8, 9)] # start at the center
    direction = 'right' # default movement is right

    print_board(snake)

    running = True
    while running:
        user_input = input("Press 'w' for up, 's' for down, 'a' for left, 'd' for right: ").lower()
        if user_input not in ['up', 'down', 'left', 'right']:
            continue

        new_snake = move_snake(snake, direction)

        board[0][1] = [['#']*(20-2)] + [[".", "."], [["#"], ["#"]]] + [[['.' for _ in range(20 - 4)] for _ in range(20 - 4)]]
        print_board(snake) # Re-print the board after each move

    return 'TERMINATE'

if __name__ == "__main__":
    main()