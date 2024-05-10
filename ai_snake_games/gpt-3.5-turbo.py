import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False
        self.alive = True

    def move(self):
        if self.alive:
            x, y = self.body[0]
            dx, dy = self.direction
            new_head = ((x + dx) % GRID_WIDTH, (y + dy) % GRID_HEIGHT)
            if new_head in self.body or new_head in walls:
                self.alive = False
            else:
                self.body.insert(0, new_head)
                if not self.grow:
                    self.body.pop()
                else:
                    self.grow = False

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def grow_snake(self):
        self.grow = True

# Food class
class Food:
    def __init__(self):
        self.position = self.new_position()

    def new_position(self):
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def eaten(self):
        self.position = self.new_position()

# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

snake = Snake()
food = Food()
walls = [(x, 0) for x in range(GRID_WIDTH)] + [(x, GRID_HEIGHT - 1) for x in range(GRID_WIDTH)] + [(0, y) for y in range(1, GRID_HEIGHT - 1)] + [(GRID_WIDTH - 1, y) for y in range(1, GRID_HEIGHT - 1)]

# Game loop
while snake.alive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            snake.alive = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(RIGHT)

    snake.move()

    if snake.body[0] == food.position:
        snake.grow_snake()
        food.eaten()

    screen.fill(BLACK)

    # Draw snake
    for segment in snake.body:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw food
    pygame.draw.ellipse(screen, RED, (food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, WHITE, (wall[0] * GRID_SIZE, wall[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()