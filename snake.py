import pygame
import random

# Game constants
WIDTH = 640
HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Snake colors
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)

    def move(self):
        x, y = self.body[0]
        dx, dy = self.direction
        new_head = ((x + dx) % GRID_WIDTH, (y + dy) % GRID_HEIGHT)
        if new_head in self.body[1:]:
            game_over()
        else:
            self.body.insert(0, new_head)
            if len(self.body) > 1 and new_head == food.position:
                food.spawn()
            else:
                self.body.pop()

    def change_direction(self, dx, dy):
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx, dy)

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(
                screen,
                SNAKE_COLOR,
                (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
            )


# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()

    def spawn(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        )

    def draw(self):
        pygame.draw.rect(
            screen,
            FOOD_COLOR,
            (
                self.position[0] * GRID_SIZE,
                self.position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            ),
        )


# Game over function
def game_over():
    pygame.quit()
    quit()


# Create objects
snake = Snake()
food = Food()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(0, -1)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(0, 1)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(-1, 0)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(1, 0)

    # Move snake
    snake.move()

    # Check for collision with food
    if snake.body[0] == food.position:
        food.spawn()

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw snake and food
    snake.draw()
    food.draw()

    # Update display
    pygame.display.update()

    # Limit frames per second
    clock.tick(FPS)

# Quit the game
pygame.quit()
