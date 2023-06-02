from setup import *
from fruit import Fruit


class Bomb(Fruit):
    RADIUS = 55

    def draw(self, surf):
        pygame.draw.circle(surf, BLACK, self.position, self.RADIUS)
