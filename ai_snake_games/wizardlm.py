import random
import pygame
import sys

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SNAKE_SIZE = 20
SQUARE_SIZE = SCREEN_WIDTH // SNAKE_SIZE

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Game class
class SnakeGame:
    def __init__(self):
        self.direction = None
        self.snake_length = 1
        self.snake_list = [[100, 100]]  # Starting position of the snake head
        self.food_pos = None
        self.game_over = False

        self.create_food()

    def create_food(self):
        self.food_pos = (random.randrange(1, (SCREEN_WIDTH // SQUARE_SIZE) - 1) * SQUARE_SIZE,
                            random.randrange(1, (SCREEN_HEIGHT // SQUARE_SIZE) - 1) * SQUARE_SIZE)

    def check_collision(self):
        # Check collision with walls and self
        game_over = False
        for segment in self.snake_list[:-1]:
            if segment[0] >= SCREEN_WIDTH or segment[0] < 0 or segment[1] >= SCREEN_HEIGHT or segment[1] < 0:
                game_over = True
        for segment in self.snake_list:
            if segment in self.snake_list[:-1]:
                game_over = True
        return game_over

    def update_snake(self):
        new_head = [self.snake_list[-1][0] + (SQUARE_SIZE * self.direction[0]),
                      self.snake_list[-1][1] + (SQUARE_SIZE * self.direction[1])]
        if new_head == self.food_pos:
            self.snake_length += 1
            self.create_food()
        self.snake_list.append(new_head)
        if len(self.snake_list) > self.snake_length:
            self.snake_list.pop(0)

    def draw(self):
        screen.fill((0, 0, 0))
        for segment in self.snake_list[:-1]:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], SQUARE_SIZE, SQUARE_SIZE))
        if self.food_pos:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.food_pos[0], self.food_pos[1], SQUARE_SIZE, SQUARE_SIZE))
        pygame.display.update()

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.direction != (1, 0):
                        self.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (0, -1):
                        self.direction = (1, 0)
                    elif event.key == pygame.K_UP and self.direction != (0, 1):
                        self.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and self.direction != (-1, 0):
                        self.direction = (0, 1)

            self.check_collision()
            self.update_snake()
            self.draw()
            clock.tick(30)  # Cap the frame rate at 30 frames per second

# Main game instance and execution
if __name__ == "__main__":
    snake_game = SnakeGame()
    snake_game.run()