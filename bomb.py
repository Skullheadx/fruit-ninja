from fruit import Fruit
from effect import SplitEffect
from setup import *


class Bomb(Fruit):
    RADIUS = 100 * SCALE.x

    EXPLOSION_RADIUS = RADIUS * 10
    POWER = 75

    BOMB_IMAGE = pygame.transform.scale(pygame.image.load("assets/bomb.png").convert_alpha(),
                                        (RADIUS * 2, RADIUS * 2)).convert_alpha()

    EXPLOSIONS = [
        [
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch1/File1.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch1/File2.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch1/File3.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch1/File4.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch1/File5.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch1/File6.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha()
        ],
        [
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch2/File1.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch2/File2.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch2/File3.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch2/File4.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch2/File5.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch2/File6.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha()
        ],
        [
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch2/File1.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch2/File2.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch2/File3.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch2/File4.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch2/File5.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(f"assets/explosion/Punch2/File6.png"),
                                   (EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)).convert_alpha()
        ],
    ]
    EXPLOSION_TIME = 500

    explosion_sound_effects = [
        pygame.mixer.Sound("assets/sounds/hq-explosion-6288.wav"),
        pygame.mixer.Sound("assets/sounds/medium-explosion-40472.wav"),
    ]

    def __init__(self):
        super().__init__()
        self.radius = self.RADIUS
        self.exploded = False
        self.exploded_frame_timer = 0
        self.image = self.BOMB_IMAGE
        self.explosion_frame = 0
        self.explosion = random.choice(self.EXPLOSIONS)

    def update(self, delta):
        super().update(delta)
        if self.exploded:
            self.exploded_frame_timer += delta
            if self.exploded_frame_timer >= self.EXPLOSION_TIME / len(self.explosion):
                self.exploded_frame_timer = 0
                self.explosion_frame = min(len(self.explosion) - 1, self.explosion_frame + 1)
                self.image = self.explosion[self.explosion_frame]
                if self.explosion_frame == len(self.explosion) - 1:
                    return True

    def explode(self, fruits, bombs, effects, depth=0):
        if self in bombs:
            if not self.exploded:
                self.image = self.explosion[0]
                if depth == 0:
                    pygame.mixer.Sound.play(random.choice(self.explosion_sound_effects))
            self.exploded = True
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

        for fruit in fruits:
            fruit.velocity += (fruit.position - self.position).normalize() * self.POWER
        for effect in effects:
            if isinstance(effect, SplitEffect):
                effect.velocity += (effect.position - self.position).normalize() * self.POWER

        for bomb in bombs:
            if not bomb.exploded:
                bomb.explode(fruits, bombs, effects,depth+1)

    def draw(self, surf):
        if self.exploded:
            surf.blit(self.image, self.image.get_rect(
                topleft=(self.position.x - self.EXPLOSION_RADIUS, self.position.y - self.EXPLOSION_RADIUS)))
        else:
            # pygame.draw.circle(surf, BLACK, self.position, self.radius)
            if self.position.y - self.radius <= HEIGHT:
                rotated_image = pygame.transform.rotate(self.image, self.angle)
                new_rect = rotated_image.get_rect(center=self.image.get_rect(
                    topleft=(self.position.x - self.radius, self.position.y - self.radius)).center)
                self.width, self.height = new_rect.size
                surf.blit(rotated_image, new_rect.topleft)
