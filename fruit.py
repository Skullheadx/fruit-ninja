import pygame

from setup import *


class Fruit:
    RADIUS_RANGE = [25, 50]

    HORIZONTAL_SPAWN_RANGE = [WIDTH / 5, WIDTH * 4 / 5]
    VERTICAL_SPAWN_RANGE = [HEIGHT + max(RADIUS_RANGE), HEIGHT*2 + max(RADIUS_RANGE) ]

    VERTICAL_TARGET_RANGE = [HEIGHT / 5, HEIGHT * 2/3]
    HORIZONTAL_TARGET_RANGE = [WIDTH / 5, WIDTH * 4 / 5]

    GRAVITY = 275

    COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    OUTLINE_WIDTH =3
    def __init__(self):
        self.radius = lerp(self.RADIUS_RANGE[0], self.RADIUS_RANGE[1], random.random())

        self.target = pygame.Vector2(lerp(self.HORIZONTAL_TARGET_RANGE[0], self.HORIZONTAL_TARGET_RANGE[1], random.random()),lerp(self.VERTICAL_TARGET_RANGE[0], self.VERTICAL_TARGET_RANGE[1], random.random()))
        self.position = pygame.Vector2(lerp(self.HORIZONTAL_SPAWN_RANGE[0], self.HORIZONTAL_SPAWN_RANGE[1], random.random()),
                                       lerp(self.VERTICAL_SPAWN_RANGE[0], self.VERTICAL_SPAWN_RANGE[1], random.random()))
        self.acceleration = pygame.Vector2(0, self.GRAVITY)


        dy = self.target.y-self.position.y
        dx = self.target.x-self.position.x
        t = (-2 / self.GRAVITY * dy)**0.5
        self.velocity = pygame.Vector2(dx/t, -(-2 * self.GRAVITY * dy)**0.5)

        self.color = random.choice(self.COLORS)

    def update(self, delta):
        self.velocity += self.acceleration * delta / 1000
        self.position += self.velocity * delta / 1000

    def get_rect(self):
        return pygame.Rect(self.position - pygame.Vector2(self.radius / 2, self.radius / 2),
                           pygame.Vector2(self.radius, self.radius))

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, self.position, self.radius)
        pygame.draw.circle(surf, DARKEN[self.color], self.position, self.radius, self.OUTLINE_WIDTH)

        # pygame.draw.circle(surf, BLACK, self.target, 10)
