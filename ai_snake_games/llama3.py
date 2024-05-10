import pygame
import random
import sys
import time
import copy

pygame.init()

WIDTH, HEIGHT = 640, 480
BLOCK_SIZE = 20
SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = 'Right'

    def move(self):
        if self.direction == 'Right':
            head = (self.body[0][0] + BLOCK_SIZE, self.body[0][1])
        elif self.direction == 'Left':
            head = (self.body[0][0] - BLOCK_SIZE, self.body[0][1])
        elif self.direction == 'Up':
            head = (self.body[0][0], self.body[0][1] - BLOCK_SIZE)
        elif self.direction == 'Down':
            head = (self.body[0][0], self.body[0][1] + BLOCK_SIZE)

        if head in self.body:
            print('Game Over! You hit yourself.')
            pygame.quit()
            sys.exit()

        self.body.insert(0, head)

    def eat(self):
        return False

class Food:
    def __init__(self):
        self.location = (random.randint(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                         random.randint(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE)
        pygame.draw.rect(screen, WHITE, (self.location[0], self.location[1], BLOCK_SIZE, BLOCK_SIZE))

    def generate(self):
        self.location = (random.randint(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                         random.randint(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE)
        pygame.draw.rect(screen, WHITE, (self.location[0], self.location[1], BLOCK_SIZE, BLOCK_SIZE))

def draw_snake(screen, snake):
    for part in snake.body:
        pygame.draw.rect(screen, WHITE, ((part[0], part[1]), (BLOCK_SIZE, BLOCK_SIZE)))

def check_collision(snake, food):
    if snake.body[-1] == food.location:
        return True
    else:
        return False

# Set up the game state
snake = Snake()
food = Food()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != 'Down':
                snake.direction = 'Up'
            elif event.key == pygame.K_DOWN and snake.direction != 'Up':
                snake.direction = 'Down'
            elif event.key == pygame.K_LEFT and snake.direction != 'Right':
                snake.direction = 'Left'
            elif event.key == pygame.K_RIGHT and snake.direction != 'Left':
                snake.direction = 'Right'

    snake.move()

    if check_collision(snake, food):
        food.generate()
            # return False

    screen.fill(BLACK)
    draw_snake(screen, snake)

    if len(snake.body) > 50:
        food.generate()

    pygame.display.update()

    for i in range(SPEED):
        time.sleep(1 / SPEED)