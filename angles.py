import pygame
import sys

class AngleSliders:
    def __init__(self, width=600, height=300):
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("3-Axis Angle Sliders")
        # Colors and font
        self.WHITE = (255, 255, 255)
        self.GREY = (180, 180, 180)
        self.BLUE = (50, 120, 255)
        self.BLACK = (0, 0, 0)
        self.FONT = pygame.font.SysFont(None, 28)
        # Create sliders
        self.sliders = [
            self.Slider(100, 40, 400, 8, 0, 360, "Base", self),
            self.Slider(100, 110, 400, 8, 0, 360, "Link1", self),
            self.Slider(100, 180, 400, 8, 0, 360, "Link2", self),
        ]
        self.clock = pygame.time.Clock()
        self.running = False

    class Slider:
        def __init__(self, x, y, w, h, min_val, max_val, name, parent):
            self.rect = pygame.Rect(x, y, w, h)
            self.min_val = min_val
            self.max_val = max_val
            self.value = min_val
            self.name = name
            self.handle_x = x  # start at left
            self.dragging = False
            self.parent = parent

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if abs(event.pos[0] - self.handle_x) < 12 and self.rect.collidepoint(event.pos):
                    self.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.handle_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
                frac = (self.handle_x - self.rect.x) / max(1, self.rect.width)
                self.value = self.min_val + frac * (self.max_val - self.min_val)

        def draw(self, surface):
            pygame.draw.rect(surface, self.parent.GREY, self.rect)
            handle_pos = (int(self.handle_x), self.rect.y + self.rect.height // 2)
            pygame.draw.circle(surface, self.parent.BLUE, handle_pos, 10)
            label = self.parent.FONT.render(f"{self.name}: {int(self.value)}°", True, self.parent.BLACK)
            surface.blit(label, (self.rect.x, self.rect.y - 30))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            for s in self.sliders:
                s.handle_event(event)

    def draw(self):
        self.WIN.fill(self.WHITE)
        for s in self.sliders:
            s.draw(self.WIN)
        pygame.display.update()

    def get_angles(self):
        """Return (base, link1, link2) in degrees as floats."""
        return tuple(s.value for s in self.sliders)

    def loop_once(self):
        """Process one frame and return current angles."""
        self.handle_events()
        self.draw()
        self.clock.tick(60)
        return self.get_angles()

    def run(self):
        """Generator that yields angles each frame while the window is open."""
        self.running = True
        while self.running:
            yield self.loop_once()
        # After exit yield final angles once
        yield self.get_angles()

    def run_blocking(self):
        """Blocking loop: runs until window is closed and returns final angles."""
        for angles in self.run():
            pass
        return self.get_angles()

if __name__ == "__main__":
    # Example usage: print angles each frame
    slider_ui = AngleSliders()
    try:
        for angles in slider_ui.run():
            print(f"Angles: base={angles[0]:.1f}, link1={angles[1]:.1f}, link2={angles[2]:.1f}")
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
        sys.exit()
