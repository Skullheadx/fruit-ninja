import random

from setup import *


class Fruit:
    SPAWN_RANGE = [WIDTH / 5, WIDTH * 4 / 5]
    VERTICAL_VELOCITY_RANGE = [-500, -350]
    HORIZONTAL_VELOCITY_RANGE = [-100, 100]
    GRAVITY = 275

    RADIUS = 50

    def __init__(self):
        self.position = pygame.Vector2(lerp(self.SPAWN_RANGE[0], self.SPAWN_RANGE[1], random.random()),
                                       HEIGHT - self.RADIUS)
        self.velocity = pygame.Vector2(
            lerp(self.HORIZONTAL_VELOCITY_RANGE[0], self.HORIZONTAL_VELOCITY_RANGE[1], random.random()),
            lerp(self.VERTICAL_VELOCITY_RANGE[0], self.VERTICAL_VELOCITY_RANGE[1], random.random()))
        self.acceleration = pygame.Vector2(0, self.GRAVITY)

    def update(self, delta):
        self.velocity += self.acceleration * delta / 1000
        self.position += self.velocity * delta / 1000

    def get_rect(self):
        return pygame.Rect(self.position - pygame.Vector2(self.RADIUS / 2, self.RADIUS / 2),
                           pygame.Vector2(self.RADIUS, self.RADIUS))

    def draw(self, surf):
        pygame.draw.circle(surf, GREEN, self.position, self.RADIUS)
