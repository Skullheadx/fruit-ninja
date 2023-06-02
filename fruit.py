from setup import *


class Fruit:
    SPAWN_RANGE = [WIDTH / 5, WIDTH * 4 / 5]
    VERTICAL_VELOCITY_RANGE = [-500, -300]
    HORIZONTAL_VELOCITY_RANGE = [-150, 150]
    GRAVITY = 275

    RADIUS_RANGE = [25, 50]

    COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

    def __init__(self):
        self.radius = lerp(self.RADIUS_RANGE[0], self.RADIUS_RANGE[1], random.random())
        self.position = pygame.Vector2(lerp(self.SPAWN_RANGE[0], self.SPAWN_RANGE[1], random.random()),
                                       HEIGHT - self.radius)
        self.velocity = pygame.Vector2(
            lerp(self.HORIZONTAL_VELOCITY_RANGE[0], self.HORIZONTAL_VELOCITY_RANGE[1], random.random()),
            lerp(self.VERTICAL_VELOCITY_RANGE[0], self.VERTICAL_VELOCITY_RANGE[1], random.random()))
        self.acceleration = pygame.Vector2(0, self.GRAVITY)
        self.color = random.choice(self.COLORS)

    def update(self, delta):
        self.velocity += self.acceleration * delta / 1000
        self.position += self.velocity * delta / 1000

    def get_rect(self):
        return pygame.Rect(self.position - pygame.Vector2(self.radius / 2, self.radius / 2),
                           pygame.Vector2(self.radius, self.radius))

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, self.position, self.radius)
