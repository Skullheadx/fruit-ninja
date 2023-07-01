from setup import *


class Fruit:
    RADIUS_RANGE = [60 * SCALE.x, 100 * SCALE.x]  # [25, 50]

    HORIZONTAL_SPAWN_RANGE = [max(RADIUS_RANGE), WIDTH - max(RADIUS_RANGE)]
    VERTICAL_SPAWN_RANGE = [HEIGHT + max(RADIUS_RANGE), HEIGHT * 2 + max(RADIUS_RANGE)]

    VERTICAL_TARGET_RANGE = [max(RADIUS_RANGE), HEIGHT * 3.5 / 5]
    HORIZONTAL_TARGET_RANGE = [WIDTH / 5.5, WIDTH * 4.5 / 5.5]

    GRAVITY = 275 * SCALE.y
    HEADS = [
        pygame.image.load(f"assets/fruits/{file}").convert_alpha() for file in os.listdir('assets/fruits/')
    ]
    OUTLINE_WIDTH = 3

    def __init__(self):
        self.radius = lerp(self.RADIUS_RANGE[0], self.RADIUS_RANGE[1], random.random())

        self.target = pygame.Vector2(
            lerp(self.HORIZONTAL_TARGET_RANGE[0], self.HORIZONTAL_TARGET_RANGE[1], random.random()),
            lerp(self.VERTICAL_TARGET_RANGE[0], self.VERTICAL_TARGET_RANGE[1], random.random()))
        self.position = pygame.Vector2(
            lerp(self.HORIZONTAL_SPAWN_RANGE[0], self.HORIZONTAL_SPAWN_RANGE[1], random.random()),
            lerp(self.VERTICAL_SPAWN_RANGE[0], self.VERTICAL_SPAWN_RANGE[1], random.random()))
        self.acceleration = pygame.Vector2(0, self.GRAVITY)

        # self.previous_position = self.position

        dy = self.target.y - self.position.y
        dx = self.target.x - self.position.x
        t = (-2 / self.GRAVITY * dy) ** 0.5
        self.velocity = pygame.Vector2(dx / t, -(-2 * self.GRAVITY * dy) ** 0.5)
        self.image = pygame.transform.scale(random.choice(self.HEADS), (self.radius * 2, self.radius * 2))
        self.angle = lerp(0, 360, random.random())
        self.direction = random.choice([-1, 1])
        # self.angle = 0
        # self.direction = 0

        self.width, self.height = (self.radius * 2, self.radius * 2)

    def update(self, delta):
        # self.previous_position = self.position.copy() - self.velocity / 1000 * 30
        self.velocity += self.acceleration * delta / 1000
        self.position += self.velocity * delta / 1000

        self.angle += 360 * delta / 1000 / 10 * self.direction

    def get_rect(self):
        return pygame.Rect(self.position - pygame.Vector2(self.radius / 2, self.radius / 2),
                           pygame.Vector2(self.radius, self.radius))

    def draw(self, surf):
        # rotated_image = pygame.transform.rotate(self.image, self.angle)
        # new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.position.x - self.radius, self.position.y - self.radius)).center)
        # surf.blit(rotated_image, new_rect.topleft)
        # pygame.draw.circle(surf, BLACK, self.position, self.radius)
        if self.position.y - self.radius <= HEIGHT:
            rotated_image, position = rotate_center(self.image, self.angle, self.position)
            self.width, self.height = rotated_image.get_size()
            surf.blit(rotated_image, position)
