import pygame
import time
import matplotlib.pyplot as plt
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLOT_WIDTH = 600
PLOT_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER_COLOR = (0, 64, 128)
GRAVITY_MIN = 1.6  # Minimum gravity to simulate Earth-like conditions
GRAVITY_MAX = 9.8  # Maximum gravity to simulate Earth-like conditions
GRAVITY_STEP = 0.1
FLOOR = 460
# Assuming you have a global variable to track simulation time
simulation_time = 0
time_scale = 0.5  # Slow down to half speed

# Physical constants
METER_TO_PIXEL = 100  # 1 meter is 100 pixels
GRAVITY = 9.81  # gravity in m/s^2
APPLE_MASS = 0.2  # mass of the apple in kg (just an example)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH + PLOT_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Apple Fall Simulation with Plot')

# Font for buttons and text
font = pygame.font.Font(None, 36)

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
        self.rect.y = 0  # Start from the top
        self.velocity_y = 0
        self.start_time = time.time()
        self.time_stopped = None
        self.positions = []
        self.velocities = []

    def update(self, gravity):
        global simulation_time
        if self.time_stopped is None:
            self.velocity_y += gravity * (1/60.0) * time_scale  # Adjust gravity by time_scale
            self.rect.y += self.velocity_y  # Update position
            # Use simulation_time instead of real time for tracking
            self.positions.append((simulation_time, self.rect.y))
            self.velocities.append((simulation_time, self.velocity_y))

            if self.rect.y >= FLOOR - self.rect.height:
                self.rect.y = FLOOR - self.rect.height
                self.velocity_y = 0
                self.time_stopped = simulation_time

    def get_time_elapsed(self):
        if self.time_stopped:
            return self.time_stopped - self.start_time
        else:
            return time.time() - self.start_time

def slow_down_action():
    global time_scale
    time_scale *= 0.5  # Halve the time_scale to slow down the simulation

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
    global simulation_time, time_scale
    simulation_time = 0  # Reset simulation time
    time_scale = 0.5  # Reset time scale
    apple.reset()

def plot_positions(positions, velocities):
    times_pos, ypos = zip(*positions)
    times_vel, vel = zip(*velocities)
    plt.figure(figsize=(8, 6))

    # Plot position
    plt.subplot(2, 1, 1)
    plt.plot(times_pos, [(FLOOR - y) / METER_TO_PIXEL for y in ypos], 'r-')  # Adjust y to make floor y=0
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.title('Apple Position Over Time')
    plt.grid(True)

    # Plot velocity
    plt.subplot(2, 1, 2)
    plt.plot(times_vel, [v / METER_TO_PIXEL for v in vel], 'b-')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Apple Velocity Over Time')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('plot.png')
    plt.close()

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
    pygame.draw.rect(screen, BLACK, (0, FLOOR, SCREEN_WIDTH, 2))

    # Display time, position, velocity, and mass
    elapsed_time = apple.get_time_elapsed()
    time_text = font.render(f"Time: {elapsed_time:.2f}s", True, BLACK)
    position_text = font.render(f"Position: ({apple.rect.x}, {apple.rect.y})", True, BLACK)
    velocity_text = font.render(f"Velocity: {apple.velocity_y:.2f}", True, BLACK)
    gravity_text = font.render(f"Gravity: {gravity_slider.value:.2f}", True, BLACK)
    meter_to_pixel_text = font.render(f"1 meter = {METER_TO_PIXEL} pixels", True, BLACK)
    mass_text = font.render(f"Apple Mass: {APPLE_MASS} kg", True, BLACK)
    screen.blit(gravity_text, (550, 480))
    screen.blit(time_text, (50, 50))
    screen.blit(position_text, (50, 100))
    screen.blit(velocity_text, (50, 150))
    screen.blit(meter_to_pixel_text, (50, 200))
    screen.blit(mass_text, (50, 250))

    # Plot positions
    if apple.positions:
        plot_positions(apple.positions, apple.velocities)
        plot_img = pygame.image.load('plot.png')
        screen.blit(plot_img, (SCREEN_WIDTH, 0))

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
