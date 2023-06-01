from setup import *


class Game:

    def __init__(self):
        pass

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return COMMAND_EXIT

    def draw(self, surf):
        screen.fill(WHITE)
