from fruit import Fruit
from effect import SplitEffect
from setup import *


class Bomb(Fruit):
    RADIUS = 100 * SCALE.x

    EXPLOSION_RADIUS = RADIUS * 10
    POWER = 75

    BOMB_IMAGE = pygame.image.load("assets/bomb.png").convert_alpha()
    BOMB_TXT = Texture.from_surface(renderer, BOMB_IMAGE)

    EXPLOSIONS = [
        [
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch1/File1.png")),
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch1/File2.png")),
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch1/File3.png")),
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch1/File4.png")),
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch1/File5.png")),
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch1/File6.png"))
        ],
        [
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch2/File1.png")),
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch2/File2.png")),
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch2/File3.png")),
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch2/File4.png")),
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch2/File5.png")),
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch2/File6.png"))
        ],
        [
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch2/File1.png")),
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch2/File2.png")),
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch2/File3.png")),
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch2/File4.png")),
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch2/File5.png")),
            Texture.from_surface(renderer, pygame.image.load(f"assets/explosion/Punch2/File6.png"))
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
        self.image = self.BOMB_IMAGE
        self.exploded = False

        self.exploded_frame_timer = 0
        self.explosion_frame = 0

        self.explosion_txt = random.choice(self.EXPLOSIONS)

    def update(self, delta):
        super().update(delta)
        if self.exploded:
            self.exploded_frame_timer += delta
            if self.exploded_frame_timer >= self.EXPLOSION_TIME / len(self.explosion_txt):
                self.exploded_frame_timer = 0
                self.explosion_frame = min(len(self.explosion_txt) - 1, self.explosion_frame + 1)
                if self.explosion_frame == len(self.explosion_txt) - 1:
                    return True

    def explode(self, fruits, bombs, effects, depth=0):
        if self in bombs:
            if not self.exploded:
                self.image = self.explosion_txt[0]
                if depth == 0:
                    pygame.mixer.Sound.play(random.choice(self.explosion_sound_effects))
            self.exploded = True
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

        for fruit in fruits:
            fruit.velocity += (fruit.position - self.position).normalize() * self.POWER
        for effect in effects:
            effect.velocity += (effect.position - self.position).normalize() * self.POWER

        for bomb in bombs:
            if not bomb.exploded:
                bomb.explode(fruits, bombs, effects, depth + 1)

    def draw(self):
        if self.exploded:
            self.explosion_txt[self.explosion_frame].draw(None, pygame.Rect(self.position.x - self.EXPLOSION_RADIUS,
                                                                            self.position.y - self.EXPLOSION_RADIUS,
                                                                            self.EXPLOSION_RADIUS * 2,
                                                                            self.EXPLOSION_RADIUS * 2))
        else:
            if self.position.y - self.radius <= HEIGHT:
                self.BOMB_TXT.draw(None, pygame.Rect(self.position.x - self.radius, self.position.y - self.radius,
                                                     self.radius * 2, self.radius * 2), self.angle,
                                   (self.radius, self.radius))
