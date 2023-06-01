from setup import *
from player import Player


class Game:

    def __init__(self):
        self.player = Player()

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return COMMAND_EXIT
        self.player.update(delta)

    def draw(self, surf):
        screen.fill(WHITE)
        self.player.draw(surf)
