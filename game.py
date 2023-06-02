from setup import *
from player import Player
from fruit import Fruit
from bomb import Bomb
from effect import Effect


class Game:
    BOMB_CHANCE = 0.1
    EFFECT_COUNT_PER_FRUIT = 10

    def __init__(self):
        self.player = Player()
        self.fruits = [Fruit()]
        self.bombs = []
        self.effects = []
        self.wave = 1

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return COMMAND_EXIT
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return COMMAND_EXIT
        self.player.update(delta)
        hits = []
        for fruit in self.fruits:
            fruit.update(delta)
            if self.player.hits(fruit):
                hits.append(fruit)
            fr = fruit.get_rect()
            if ((not -fruit.radius < fr.x < WIDTH + fruit.radius) or fr.y > HEIGHT) and fruit.velocity.y > 0:
                self.fruits.remove(fruit)

        for hit in hits:
            for i in range(self.EFFECT_COUNT_PER_FRUIT):
                self.effects.append(Effect(hit.position, hit.radius, hit.color))
            if hit in self.fruits:
                self.fruits.remove(hit)

        for effect in self.effects:
            effect_status = effect.update(delta)
            if effect_status:
                self.effects.remove(effect)

        for bomb in self.bombs:
            bomb.update(delta)
            if self.player.hits(bomb):
                return COMMAND_START
            br = bomb.get_rect()
            if ((not -bomb.RADIUS < br.x < WIDTH + bomb.RADIUS) or br.y > HEIGHT) and bomb.velocity.y > 0:
                self.bombs.remove(bomb)

        if len(self.fruits) == 0 and len(self.bombs) == 0:
            self.wave += 1
            for i in range(self.wave):
                if random.random() < self.BOMB_CHANCE:
                    self.bombs.append(Bomb())
                else:
                    self.fruits.append(Fruit())

    def draw(self, surf):
        screen.fill(BROWN)
        for effect in self.effects:
            effect.draw(surf)
        for fruit in self.fruits:
            fruit.draw(surf)
        for bomb in self.bombs:
            bomb.draw(surf)
        self.player.draw(surf)
