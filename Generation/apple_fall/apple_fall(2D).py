import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAVITY = 0.5

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Apple Fall Simulation')

# Apple class
class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0
        self.velocity_y = 0

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.velocity_y = 0

# Create an apple
apple = Apple()

# Create a sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(apple)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the apple
    all_sprites.update()

    # Clear the screen
    screen.fill(WHITE)

    # Draw all sprites
    all_sprites.draw(screen)

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
