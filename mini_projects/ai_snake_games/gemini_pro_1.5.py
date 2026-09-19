import pygame
import random

# Initialize Pygame
pygame.init()

# Set window dimensions
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Snake properties
snake_block_size = 10
snake_speed = 15

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Font for displaying score
font_style = pygame.font.SysFont(None, 30)


def display_score(score):
    value = font_style.render("Your Score: " + str(score), True, green)
    screen.blit(value, [0, 0])


def draw_snake(snake_block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], snake_block_size, snake_block_size])


def game_loop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    # Initialize x1_change to start movement (rightward in this case)
    x1_change = snake_block_size
    y1_change = 0

    snake_list = []
    snake_length = 1

    foodx = round(random.randrange(0, width - snake_block_size) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block_size) / 10.0) * 10.0

    while not game_over:
        while game_close:
            screen.fill(black)
            message = font_style.render("You Lost! Press Q-Quit or C-Play Again", True, red)
            screen.blit(message, [width / 6, height / 3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block_size:
                    x1_change = -snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block_size:
                    x1_change = snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block_size:
                    y1_change = -snake_block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block_size:
                    y1_change = snake_block_size
                    x1_change = 0

            if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
                game_close = True

            x1 += x1_change
            y1 += y1_change
            screen.fill(black)
            pygame.draw.rect(screen, red, [foodx, foody, snake_block_size, snake_block_size])
            snake_head = [x1, y1]
            snake_list.append(snake_head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True

            draw_snake(snake_block_size, snake_list)
            display_score(snake_length - 1)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, width - snake_block_size) / 10.0) * 10.0
                foody = round(random.randrange(0, height - snake_block_size) / 10.0) * 10.0
                snake_length += 1

            clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()
