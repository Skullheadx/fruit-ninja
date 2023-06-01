from setup import *
from player import Player
from fruit import Fruit


class Game:

    def __init__(self):
        self.player = Player()
        self.fruits = [Fruit()]

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

        for hit in hits:
            self.fruits.remove(hit)

    def draw(self, surf):
        screen.fill(WHITE)
        for fruit in self.fruits:
            fruit.draw(surf)
        self.player.draw(surf)
