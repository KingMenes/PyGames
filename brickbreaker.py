import pygame
import random

# Game constants
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_PADDING = 10
FPS = 90

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Game variables
score = 0
lives = 3


# Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = (WIDTH - PADDLE_WIDTH) // 2
        self.rect.y = HEIGHT - PADDLE_HEIGHT - 10
        self.speed = 8

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - PADDLE_WIDTH:
            self.rect.x += self.speed


# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.image.fill(RED)
        pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2
        self.speed_x = random.choice([-2, 2])
        self.speed_y = -2

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Check collision with walls
        if self.rect.x <= 0 or self.rect.x >= WIDTH - BALL_RADIUS * 2:
            self.speed_x *= -1
        if self.rect.y <= 0:
            self.speed_y *= -1

        # Check collision with paddle
        if pygame.sprite.collide_rect(self, paddle):
            self.speed_y *= -1

        # Check collision with bricks
        brick_collision = pygame.sprite.spritecollide(self, bricks, True)
        if brick_collision:
            self.speed_y *= -1
            global score
            score += 1

        # Check if ball goes out of bounds
        if self.rect.y >= HEIGHT:
            global lives
            lives -= 1
            self.rect.x = WIDTH // 2
            self.rect.y = HEIGHT // 2
            self.speed_x = random.choice([-2, 2])
            self.speed_y = -2


# Brick class
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Create sprites
all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()
paddle = Paddle()
ball = Ball()

all_sprites.add(paddle)
all_sprites.add(ball)

# Create bricks
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = Brick(
            col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING,
            row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_PADDING,
        )
        all_sprites.add(brick)
        bricks.add(brick)


# Game over function
def game_over():
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over", True, YELLOW)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    quit()


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    screen.fill(BLACK)

    all_sprites.draw(screen)

    # Draw score and lives
    font = pygame.font.Font(None, 30)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))

    if len(bricks) == 0:
        game_over()

    if lives == 0:
        game_over()

    pygame.display.update()
    clock.tick(FPS)

# Quit the game
pygame.quit()
