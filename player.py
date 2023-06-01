from setup import *


class Player:
    LIFE_TIME = 100

    def __init__(self):
        self.sliced = []

    def update(self, delta):
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            pos = pygame.mouse.get_pos()
            self.sliced.append((pos, pygame.time.get_ticks()))
        else:
            self.sliced.clear()
        for i, val in enumerate(self.sliced):
            pos, time = val
            if pygame.time.get_ticks() - time > self.LIFE_TIME:
                self.sliced.pop(i)
                break

    def draw(self, surf):
        for pos, time in self.sliced:
            pygame.draw.circle(surf, RED, pos, 10)
        if len(self.sliced) > 1:
            pygame.draw.lines(surf, BLACK, False, [a for a, b in self.sliced], 10)
