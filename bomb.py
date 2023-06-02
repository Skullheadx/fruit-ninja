from fruit import Fruit
from setup import *


class Bomb(Fruit):
    RADIUS = 55

    EXPLOSION_RADIUS = 100
    POWER = 75

    def __init__(self):
        super().__init__()
        self.radius = self.RADIUS
        self.exploded = False
        self.exploded_time = 0

    def update(self, delta):
        super().update(delta)
        if self.exploded:
            self.exploded_time += delta ** 2

    def explode(self, fruits, bombs):
        if self in bombs:
            self.exploded = True
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

        for fruit in fruits:
            fruit.velocity += (fruit.position - self.position).normalize() * self.POWER
        for bomb in bombs:
            if not bomb.exploded:
                bomb.explode(fruits, bombs)

    def draw(self, surf):
        if self.exploded:
            pygame.draw.circle(surf, DARK_RED, self.position,
                               clamp(self.RADIUS + self.exploded_time / 1000 * 100, 0, 300))
            pygame.draw.circle(surf, BLACK, self.position, clamp(self.RADIUS + self.exploded_time / 1000 * 100, 0, 300),
                               self.OUTLINE_WIDTH)
        else:
            pygame.draw.circle(surf, BLACK, self.position, self.RADIUS)
