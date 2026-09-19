import sys
import random

# Initialize Pygame
pygame.init()

# Window settings
SCREEN_WIDTH   = 800
SCREEN_HEIGHT    = 600

# Snake class
class Snake:
    def __init__(self):
        self.segments = [((SCREEN_WIDTH - 100) // 40), ((SCREEN_HEIGHT - 200) // 30)))]  # Initial segments in the form of (x, y))
        self.head = self.segments[0]

    def move(self, direction):
        new_head = self.move_owards_head(direction)

        if new_head:
            segments_to_remove = [seg for seg in self.segments[:-1] if (seg[0], seg[1]) == (new_head[0], new_head[1]))]]   # Remove segments that overlap with the new head
            segments_to_add = [(new_head[0]), (new_head[1])))]]   # Add segments for the new head

            self.segments = self.segments[:len(segments_to_remove))].extend(segments_to_remove).append(segments_to_add[0]))  # Update segments list
        return new_head

    def move_owards_head(self, direction):
        head_x, head_y = self.head[0], self.head[1]

        if direction == 'UP':
            return (head_x, head_y - 1), True
        elif direction == 'DOWN':
            return (head_x, head_y + 1), True
        elif direction == 'LEFT':
            return (head_x - 1, head_y)), True
        elif direction == 'RIGHT':
            return (head_x + 1, head_y)), True

        return None, False   # If the direction is invalid, return None and False

# Score class
class Score:
    def __init__(self):
        self.score = 0
        self.text_surface = None

    def update_score(self, new_score):
        self.score += new_score

    def create_text_surface(self, text, font_size=24, color=WHITE)):
        self.text_surface = pygame.Surface((font_size * len(text)), 30)).convert_alpha()

        for char in text:
            if char == ' ':    # Add space between characters
                rect = pygame.Rect(0, (font_size - 1) // 2), font_size  // 4  - 1)
                pygame.draw.rect(self.text_surface, WHITE, rect))
                rect.move_ip((font_size - 1) // 2  - 1), font_size  // 4)
            else:
                rect = pygame.Rect(0, (font_size - 5) // 2), font_size  // 8  - 1)
                font_char = pygame.font.SysFont("Arial", font_size  // 3)).render(char, False, WHITE))
                pygame.draw.rect(self.text_surface, BLACK, rect))
                self.text_surface.blit(font_char, (rect.width  - font_char.get_width())  // 2)))

    def draw_text_surface_on_屏幕(self):
        screen.blit(self.text_surface, ((SCREEN_WIDTH - self.text_surface.get_width()))  // 2),  (SCREEN_HEIGHT - self.text_surface.get_height() // 2) ))