from setup import *


class Fruit:
    RADIUS_RANGE = [60 * SCALE.x, 100 * SCALE.x]

    HORIZONTAL_SPAWN_RANGE = [max(RADIUS_RANGE), WIDTH - max(RADIUS_RANGE)]
    VERTICAL_SPAWN_RANGE = [HEIGHT + max(RADIUS_RANGE), HEIGHT * 2 + max(RADIUS_RANGE)]

    VERTICAL_TARGET_RANGE = [max(RADIUS_RANGE), HEIGHT * 3.5 / 5]
    HORIZONTAL_TARGET_RANGE = [WIDTH / 5.5, WIDTH * 4.5 / 5.5]

    GRAVITY = 275 * SCALE.y
    FRUITS = [
        pygame.image.load(f"assets/fruits/{file}").convert_alpha() for file in os.listdir('assets/fruits/')
    ]

    def __init__(self):
        self.radius = lerp(self.RADIUS_RANGE[0], self.RADIUS_RANGE[1], random.random())

        self.target = pygame.Vector2(
            lerp(self.HORIZONTAL_TARGET_RANGE[0], self.HORIZONTAL_TARGET_RANGE[1], random.random()),
            lerp(self.VERTICAL_TARGET_RANGE[0], self.VERTICAL_TARGET_RANGE[1], random.random()))
        self.position = pygame.Vector2(
            lerp(self.HORIZONTAL_SPAWN_RANGE[0], self.HORIZONTAL_SPAWN_RANGE[1], random.random()),
            lerp(self.VERTICAL_SPAWN_RANGE[0], self.VERTICAL_SPAWN_RANGE[1], random.random()))

        self.acceleration = pygame.Vector2(0, self.GRAVITY)

        dy = self.target.y - self.position.y
        dx = self.target.x - self.position.x
        t = (-2 / self.GRAVITY * dy) ** 0.5
        self.velocity = pygame.Vector2(dx / t, -(-2 * self.GRAVITY * dy) ** 0.5)

        self.angle = lerp(0, 360, random.random())
        self.direction = random.choice([-1, 1])

        self.width, self.height = (self.radius * 2, self.radius * 2)

        self.image = random.choice(self.FRUITS)
        self.fruit_txt = Texture.from_surface(renderer, self.image)

    def update(self, delta):
        self.velocity += self.acceleration * delta / 1000
        self.position += self.velocity * delta / 1000

        self.angle += 360 * delta / 1000 / 10 * self.direction

    def draw(self):
        if self.position.y - self.radius <= HEIGHT:
            self.fruit_txt.draw(None, pygame.Rect(self.position - pygame.Vector2(self.radius, self.radius),
                                                  (self.radius * 2, self.radius * 2)),
                                angle=self.angle, origin=(self.radius, self.radius))
