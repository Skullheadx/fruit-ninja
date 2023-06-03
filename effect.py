from setup import *


class Effect:
    LIFE_TIME = 750
    SPEED_RANGE = [250, 350]
    RADIUS_RANGE = [0.25, 0.75]

    OUTLINE_WIDTH = 1

    def __init__(self, position, radius, color, darken=True):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(random.random() - 0.5, random.random() - 0.5).normalize() * lerp(
            self.SPEED_RANGE[0], self.SPEED_RANGE[1], random.random())
        self.radius = radius * lerp(self.RADIUS_RANGE[0], self.RADIUS_RANGE[1], random.random())
        self.time = self.LIFE_TIME
        if darken:
            self.color = DARKEN[color]
            self.outline_color = color
        else:
            self.color = color
            self.outline_color = DARKEN[color]

    def update(self, delta):
        self.position += self.velocity * delta / 1000
        self.time -= delta
        if self.time <= 0:
            return True

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, self.position, self.radius)
        pygame.draw.circle(surf, self.outline_color, self.position, self.radius, self.OUTLINE_WIDTH)
