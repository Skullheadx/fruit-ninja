from setup import *


class ComboCounter:
    LIFE_TIME = 1000

    def __init__(self, position, combo):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, -100)
        self.time = self.LIFE_TIME
        self.combo = combo
        self.text_surface = font_large.render(self.combo, True, BLACK)

    def update(self, delta):
        self.position += self.velocity * delta / 1000
        self.time -= delta
        if self.time <= 0:
            return True

    def draw(self, surf):
        surf.blit(self.text_surface, self.position)
