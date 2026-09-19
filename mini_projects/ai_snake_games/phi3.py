import pygame
import random
import time

# Initialize Pygame
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 70, 60)
green = (0, 255, 0)
blue = (51, 153, 255)

dis_width = 800
dis_height  = 600

game_dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)

def game_loop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_block = 10
    snake_length = 1

    fruit_position = [dis_width / 2, dis_height / 2]

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1 -= snake_block
                    y1 -= snake_block
                    x1_change = -snake_block
                    y1_change = 0

                elif event.key == pygame.K_RIGHT:
                    x1 += snake_block
                    y1 += snake_block
                    x1_change = snake_block
                    y1_change = 0

                elif event.key == pygame.K_UP:
                    x1 -= 0
                    y1 -= snake_block
                    x1_change = 0
                    y1_change = -snake_block

                elif event.key == pygame.K_DOWN:
                    x1 += 0
                    y1 += snake_block
                    x1_change = 0
                    y1_change = snake_block

        # This is to keep the game from ending when hitting a side of the screen.
        if x1 < 0 or x1 > dis_width or y1 < 0 or y1 > dis_height:
            game_over = True

        y1 += y1_change
        x1 += x1_change

        game_dis.fill(blue)

        pygame.draw.rect(game_dis, white, [40, 40, snake_block, snake_block])

        if x1 >= dis_width - fruit_position[0] and y1 >= dis_height - fruit_position[1]:
            fruit_position = [x1 - snake_block, y1 - snake_block]
            snake_length += 1

        for i in range(snake_length-1):
            if x1 == snake_block:
                pygame.draw.rect(game_dis, green, [x1 - (i + 1) * snake_block, y1 - snake_block])
            elif y1 == snake_block:
                pygame.draw.rect(game_dis, green, [x1 - snake_block, y1 - (i+1) *snake_block])

        pygame.display.update()

        clock.tick(30)

    # Terminate the game loop once it is done.
    return 'TERMINATE'

game_loop()