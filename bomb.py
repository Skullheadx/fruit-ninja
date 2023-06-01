from setup import *
from fruit import Fruit


class Bomb(Fruit):
    RADIUS = 35
    def draw(self, surf):
        pygame.draw.circle(surf, BLACK, self.position, self.RADIUS)
