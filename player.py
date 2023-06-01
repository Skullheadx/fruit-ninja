from setup import *


class Player:
    LIFE_TIME = 100
    INFLATE_SCALE = 20

    def __init__(self):
        self.sliced_points = []
        self.hitboxes = []

    def update(self, delta):
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            pos = pygame.mouse.get_pos()
            self.sliced_points.append((pygame.Vector2(pos), pygame.time.get_ticks()))
        for i, val in enumerate(self.sliced_points):
            pos, time = val
            if pygame.time.get_ticks() - time > self.LIFE_TIME:
                self.sliced_points.pop(i)
                break
        if len(self.sliced_points) > 1:
            self.hitboxes.clear()
            for i in range(len(self.sliced_points) - 1):
                self.hitboxes.append(pygame.Rect(self.sliced_points[i][0],
                                                 (self.sliced_points[i][0] - self.sliced_points[i + 1][0])).inflate(
                    self.INFLATE_SCALE, self.INFLATE_SCALE))

    def hits(self, fruit):
        for hitbox in self.hitboxes:
            if hitbox.colliderect(fruit.get_rect()):
                return True
        return False

    def draw(self, surf):
        for hitbox in self.hitboxes:
            pygame.draw.rect(surf, RED, hitbox)
        # for pos, time in self.sliced_points:
        #     pygame.draw.circle(surf, RED, pos, 10)
        # if len(self.sliced_points) > 1:
        #     pygame.draw.lines(surf, BLACK, False, [a for a, b in self.sliced_points], 3)
