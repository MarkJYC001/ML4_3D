import pygame
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER_COLOR = (0, 64, 128)
GRAVITY_MIN = 0.1
GRAVITY_MAX = 0.5  # Lower gravity to slow down the fall
GRAVITY_STEP = 0.05

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Apple Fall Simulation')

# Font for buttons and text
font = pygame.font.Font(None, 36)
floor = 460




# Apple class
class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))  # Make the apple smaller
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.reset()
    
    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2  # Place the apple in the middle
        self.rect.y = 0 # Start from the top
        self.velocity_y = 0
        self.start_time = time.time()
        self.time_stopped = None

    def update(self, gravity):
        if self.time_stopped is None:
            self.velocity_y += gravity
            self.rect.y += self.velocity_y  # Falling upwards since y=0 is the floor

            if self.rect.y >= floor - self.rect.height :
                self.rect.y = floor - self.rect.height
                self.velocity_y = 0
                self.time_stopped = time.time()

    def get_time_elapsed(self):
        if self.time_stopped:
            return min(time.time() - self.start_time, self.time_stopped - self.start_time + 5)
        else:
            return time.time() - self.start_time

# Button class
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
    
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER_COLOR if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.action()

# Slider class
class Slider:
    def __init__(self, x, y, width, min_val, max_val, step):
        self.rect = pygame.Rect(x, y, width, 20)
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.value = (min_val + max_val) / 2
        self.handle_rect = pygame.Rect(0, y - 10, 10, 40)
        self.dragging = False
        self.update_handle()

    def update_handle(self):
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.handle_rect.centerx = self.rect.left + ratio * self.rect.width

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        pygame.draw.rect(screen, BUTTON_COLOR, self.handle_rect)
        self.update_handle()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.handle_rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_rect.centerx = max(self.rect.left, min(event.pos[0], self.rect.right))
            ratio = (self.handle_rect.centerx - self.rect.left) / self.rect.width
            self.value = self.min_val + ratio * (self.max_val - self.min_val)
            self.value = round(self.value / self.step) * self.step

# Action functions
def restart_action():
    apple.reset()

def slow_down_action():
    global clock
    clock.tick(10)

# Create an apple
apple = Apple()

# Create buttons
buttons = [
    Button(50, 500, 200, 50, 'Restart', restart_action),
    Button(300, 500, 200, 50, 'Slow Down', slow_down_action)
]

# Create slider
gravity_slider = Slider(550, 510, 200, GRAVITY_MIN, GRAVITY_MAX, GRAVITY_STEP)

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
        gravity_slider.handle_event(event)

    # Update the apple
    all_sprites.update(gravity_slider.value)

    # Clear the screen
    screen.fill(WHITE)

    # Draw all sprites
    all_sprites.draw(screen)

    # Draw buttons
    for button in buttons:
        button.draw(screen)
        button.check_click()

    # Draw slider
    gravity_slider.draw(screen)

    # Draw the floor
    pygame.draw.rect(screen, BLACK, (0, floor, SCREEN_WIDTH, 2))

    # Display time, position, and velocity
    elapsed_time = apple.get_time_elapsed()
    time_text = font.render(f"Time: {elapsed_time:.2f}s", True, BLACK)
    position_text = font.render(f"Position: ({apple.rect.x}, {apple.rect.y})", True, BLACK)
    velocity_text = font.render(f"Velocity: {apple.velocity_y:.2f}", True, BLACK)
    gravity_text = font.render(f"Gravity: {gravity_slider.value:.2f}", True, BLACK)
    screen.blit(gravity_text, (550, 480))
    screen.blit(time_text, (50, 50))
    screen.blit(position_text, (50, 100))
    screen.blit(velocity_text, (50, 150))

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()


