from setup import *


class Effect:
    LIFE_TIME = 500
    SPEED_RANGE = [150, 250]
    RADIUS_RANGE = [0.25, 0.75]
    DARKEN = {RED: DARK_RED, ORANGE: DARK_ORANGE, YELLOW: DARK_YELLOW, GREEN: DARK_GREEN, BLUE: DARK_BLUE, PURPLE: DARK_PURPLE}

    def __init__(self, position, radius, color):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(random.random() - 0.5, random.random() - 0.5).normalize() * lerp(
            self.SPEED_RANGE[0],self.SPEED_RANGE[1],random.random())
        self.radius = radius * lerp(self.RADIUS_RANGE[0], self.RADIUS_RANGE[1], random.random())
        self.time = self.LIFE_TIME
        self.color = self.DARKEN[color]

    def update(self, delta):
        self.position += self.velocity * delta / 1000
        self.time -= delta
        if self.time <= 0:
            return True

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, self.position, self.radius)
