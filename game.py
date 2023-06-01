from setup import *
from player import Player
from fruit import Fruit
from bomb import Bomb


class Game:
    BOMB_CHANCE = 0.5

    def __init__(self):
        self.player = Player()
        self.fruits = [Fruit()]
        self.bombs = []
        self.wave = 1

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return COMMAND_EXIT
        self.player.update(delta)
        hits = []
        for fruit in self.fruits:
            fruit.update(delta)
            if self.player.hits(fruit):
                hits.append(fruit)
            fr = fruit.get_rect()
            if (not -fruit.radius <= fr.x < WIDTH) or fr.y > HEIGHT:
                self.fruits.remove(fruit)

        for hit in hits:
            self.fruits.remove(hit)

        for bomb in self.bombs:
            bomb.update(delta)
            if self.player.hits(bomb):
                return COMMAND_START
            br = bomb.get_rect()
            if (not -bomb.RADIUS <= br.x < WIDTH) or br.y > HEIGHT:
                self.bombs.remove(bomb)

        if len(self.fruits) == 0:
            self.wave += 1
            for i in range(self.wave):
                if random.random() < self.BOMB_CHANCE:
                    self.bombs.append(Bomb())
                else:
                    self.fruits.append(Fruit())

    def draw(self, surf):
        screen.fill(WHITE)
        for fruit in self.fruits:
            fruit.draw(surf)
        for bomb in self.bombs:
            bomb.draw(surf)
        self.player.draw(surf)
