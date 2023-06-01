from setup import *
from player import Player
from fruit import Fruit


class Game:

    def __init__(self):
        self.player = Player()
        self.fruits = [Fruit()]
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

        if len(self.fruits) == 0:
            self.wave += 1
            for i in range(self.wave):
                self.fruits.append(Fruit())

    def draw(self, surf):
        screen.fill(WHITE)
        for fruit in self.fruits:
            fruit.draw(surf)
        self.player.draw(surf)
