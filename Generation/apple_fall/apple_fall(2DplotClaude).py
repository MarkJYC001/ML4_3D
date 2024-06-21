import pygame
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SIM_WIDTH = 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER_COLOR = (0, 64, 128)
GRAVITY_MIN = 9.0
GRAVITY_MAX = 10.0
GRAVITY_STEP = 0.1
FLOOR_HEIGHT = 700

# Physical constants
METER_TO_PIXEL = 100  # 1 meter is 100 pixels
GRAVITY = 9.81  # m/s^2
APPLE_MASS = 0.1  # kg
APPLE_RADIUS = 0.1  # m

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Apple Fall Simulation')

font = pygame.font.Font(None, 36)

class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = APPLE_RADIUS * METER_TO_PIXEL
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.reset()
    
    def reset(self):
        self.rect.centerx = SIM_WIDTH // 2
        self.y = 0  # Start at 0 meters (top)
        self.velocity_y = 0
        self.start_time = time.time()
        self.time_stopped = None
        self.positions = []
        self.velocities = []

    def update(self, gravity, dt):
        if self.time_stopped is None:
            self.velocity_y += gravity * dt
            self.y += self.velocity_y * dt
            self.rect.bottom = FLOOR_HEIGHT - (self.y * METER_TO_PIXEL)

            current_time = time.time() - self.start_time
            self.positions.append((current_time, self.y))
            self.velocities.append((current_time, self.velocity_y))

            if self.rect.bottom >= FLOOR_HEIGHT:
                self.rect.bottom = FLOOR_HEIGHT
                self.y = (FLOOR_HEIGHT - self.rect.bottom) / METER_TO_PIXEL
                self.velocity_y = 0
                self.time_stopped = time.time()

    def get_time_elapsed(self):
        return self.time_stopped - self.start_time if self.time_stopped else time.time() - self.start_time

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

def restart_action():
    apple.reset()

def plot_data(positions, velocities):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(4, 6))
    fig.suptitle('Apple Motion')

    times_pos, ypos = zip(*positions)
    times_vel, vel = zip(*velocities)

    ax1.plot(times_pos, ypos, 'r-')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Height (m)')
    ax1.set_title('Height vs Time')
    ax1.grid(True)

    ax2.plot(times_vel, vel, 'b-')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Velocity (m/s)')
    ax2.set_title('Velocity vs Time')
    ax2.grid(True)

    plt.tight_layout()
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    plt.close(fig)

    return pygame.image.fromstring(raw_data, size, "RGB")

apple = Apple()
buttons = [Button(50, 750, 200, 40, 'Restart', restart_action)]
gravity_slider = Slider(300, 760, 200, GRAVITY_MIN, GRAVITY_MAX, GRAVITY_STEP)
all_sprites = pygame.sprite.Group(apple)

running = True
clock = pygame.time.Clock()
plot_surface = None

while running:
    dt = clock.tick(60) / 1000.0  # Time passed in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        gravity_slider.handle_event(event)

    all_sprites.update(gravity_slider.value, dt)

    screen.fill(WHITE)
    
    # Draw simulation area
    pygame.draw.rect(screen, (240, 240, 240), (0, 0, SIM_WIDTH, SCREEN_HEIGHT))
    all_sprites.draw(screen)

    for button in buttons:
        button.draw(screen)
        button.check_click()

    gravity_slider.draw(screen)

    # Draw floor
    # pygame.draw.rect(screen, BLACK, (0, FLOOR_HEIGHT, SIM_WIDTH, SCREEN_HEIGHT - FLOOR_HEIGHT))

    elapsed_time = apple.get_time_elapsed()
    time_text = font.render(f"Time: {elapsed_time:.2f}s", True, BLACK)
    position_text = font.render(f"Height: {apple.y:.2f}m", True, BLACK)
    velocity_text = font.render(f"Velocity: {apple.velocity_y:.2f}m/s", True, BLACK)
    gravity_text = font.render(f"Gravity: {gravity_slider.value:.2f}m/s²", True, BLACK)
    mass_text = font.render(f"Apple Mass: {APPLE_MASS}kg", True, BLACK)

    screen.blit(time_text, (50, 50))
    screen.blit(position_text, (50, 100))
    screen.blit(velocity_text, (50, 150))
    screen.blit(gravity_text, (300, 730))
    screen.blit(mass_text, (50, 200))

    if apple.positions:
        plot_surface = plot_data(apple.positions, apple.velocities)
        screen.blit(plot_surface, (SIM_WIDTH, 0))

    pygame.display.flip()

pygame.quit()