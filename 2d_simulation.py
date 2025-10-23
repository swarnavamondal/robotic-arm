import pygame
import sys
import math

pygame.init()

# Window setup
WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3-Link Arm with Sliders")

# Colors
WHITE = (255, 255, 255)
GREY = (180, 180, 180)
BLUE = (50, 120, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)

# Font
FONT = pygame.font.SysFont(None, 28)

# Slider class
class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, name):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = 0
        self.name = name
        self.handle_x = x
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if abs(event.pos[0] - self.handle_x) < 10 and self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.handle_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
                self.value = (self.handle_x - self.rect.x) / self.rect.width * (self.max_val - self.min_val)

    def draw(self, surface):
        # Draw line
        pygame.draw.rect(surface, GREY, self.rect)
        # Draw handle
        handle_pos = (int(self.handle_x), self.rect.y + self.rect.height // 2)
        pygame.draw.circle(surface, BLUE, handle_pos, 10)
        # Draw label
        label = FONT.render(f"{self.name}: {int(self.value)}°", True, BLACK)
        surface.blit(label, (self.rect.x, self.rect.y - 30))

# Create sliders
base_slider = Slider(150, 450, 500, 8, 0, 360, "Base")
link1_slider = Slider(150, 500, 500, 8, 0, 360, "Link1")
link2_slider = Slider(150, 550, 500, 8, 0, 360, "Link2")

sliders = [base_slider, link1_slider, link2_slider]

# Arm parameters
L1 = 362  # length of first link
L2 = 290  # length of second link
origin = (WIDTH // 2, HEIGHT // 2 - 50)  # base position

# Draw robotic arm
def draw_arm(surface, base_angle, th1, th2):
    # Convert to radians
    base_rad = math.radians(base_angle)
    th1_rad = math.radians(th1)
    th2_rad = math.radians(th2)

    # Base rotation direction
    dir_x = math.cos(base_rad)
    dir_y = math.sin(base_rad)

    # First joint position
    x1 = origin[0] + L1 * math.cos(th1_rad) * dir_x
    y1 = origin[1] - L1 * math.sin(th1_rad)

    # Second joint position
    x2 = x1 + L2 * math.cos(th1_rad + th2_rad) * dir_x
    y2 = y1 - L2 * math.sin(th1_rad + th2_rad)

    # Draw base
    pygame.draw.circle(surface, BLACK, origin, 10)
    # Draw links
    pygame.draw.line(surface, BLUE, origin, (x1, y1), 6)
    pygame.draw.line(surface, RED, (x1, y1), (x2, y2), 6)
    # Draw joints
    pygame.draw.circle(surface, BLACK, (int(x1), int(y1)), 8)
    pygame.draw.circle(surface, BLACK, (int(x2), int(y2)), 8)

# Main loop
clock = pygame.time.Clock()

while True:
    WIN.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for slider in sliders:
            slider.handle_event(event)

    # Draw sliders
    for slider in sliders:
        slider.draw(WIN)

    # Draw arm visualization
    draw_arm(WIN, base_slider.value, link1_slider.value, link2_slider.value)

    pygame.display.update()
    clock.tick(60)
