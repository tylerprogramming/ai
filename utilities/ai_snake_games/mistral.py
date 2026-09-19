import random
import pygame

WIDTH = 800
HEIGHT = 600
SNAKE_SPEED = 10
APPLE_SIZE = 25

class Snake:
    def __init__(self):
        self.snake_parts = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (0, -SNAKE_SPEED)
        self.length = 1

    @staticmethod
    def _distance(p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    def move(self):
        head = self.snake_parts[-1]  # Get the current head position
        new_head = (head[0] + self.direction[0],
                    head[1] + self.direction[1])  # Calculate the new head position based on the direction
        self.snake_parts.append(new_head)

    def check_collision(self, apple):
        for i in range(len(self.snake_parts) - 1, 0, -1):
            if self._distance(self.snake_parts[i], apple) < APPLE_SIZE + 1:
                print("Collision detected! Game over.")
                pygame.quit()

        if self._distance(apple, self.snake_parts[-1]) < APPLE_SIZE:
            self.length += 1
            apple = self._generate_new_food(apple)

    def _generate_new_food(self, old_apple):
        while True:
            x = random.randint(0, WIDTH // APPLE_SIZE - 1) * APPLE_SIZE + APPLE_SIZE / 2
            y = random.randint(0, HEIGHT // APPLE_SIZE - 1) * APPLE_SIZE + APPLE_SIZE / 2
            if (x, y) != old_apple:
                return (x, y)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 24)

apple = (random.randint(0, WIDTH // APPLE_SIZE - 1) * APPLE_SIZE + APPLE_SIZE / 2, random.randint(0, HEIGHT // APPLE_SIZE - 1) * APPLE_SIZE + APPLE_SIZE / 2)
snake = Snake()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake.direction = (-1, 0)
    elif keys[pygame.K_RIGHT]:
        snake.direction = (1, 0)
    elif keys[pygame.K_UP]:
        snake.direction = (0, -1)
    elif keys[pygame.K_DOWN]:
        snake.direction = (0, 1)

    snake.move()
    snake.check_collision(apple)

    screen.fill((255, 255, 255))
    for part in snake.snake_parts:
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(part[0], part[1], APPLE_SIZE, APPLE_SIZE))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(apple[0], apple[1], APPLE_SIZE, APPLE_SIZE))
    label = font.render("Length: {}".format(snake.length), False, (0, 0, 0))
    screen.blit(label, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()