import pygame
import sys
import random

# Initialize the game engine
pygame.init()

# Define the game screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define the snake's initial position
snake_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]

# Define the snake's direction
snake_dir = 'up'

# Define the food's position
food_pos = [0, 0]

# Define the game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle keypresses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake_dir = 'up'
            elif event.key == pygame.K_DOWN:
                snake_dir = 'down'
            elif event.key == pygame.K_LEFT:
                snake_dir = 'left'
            elif event.key == pygame.K_RIGHT:
                snake_dir = 'right'

    # Update the snake's position
    if snake_dir == 'up':
        snake_pos[1] -= 1
    elif snake_dir == 'down':
        snake_pos[1] += 1
    elif snake_dir == 'left':
        snake_pos[0] -= 1
    elif snake_dir == 'right':
        snake_pos[0] += 1

    # Check if the snake has hit the side of the screen
    if snake_pos[0] < 0 or snake_pos[0] >= SCREEN_WIDTH or snake_pos[1] < 0 or snake_pos[1] >= SCREEN_HEIGHT:
        running = False



    # Render the game screen
    screen.fill((0, 0, 0))
    food_pos = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
    pygame.draw.circle(screen, (255, 255, 0), snake_pos, 10)
    pygame.draw.circle(screen, (255, 0, 0), food_pos, 5)
    pygame.display.update()

# Quit the game engine
pygame.quit()
sys.exit()