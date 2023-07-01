import pygame

from setup import *


class Player:
    LIFE_TIME = 100
    INFLATE_SCALE = 20

    IMAGE = pygame.image.load("assets/effects/sword_slashes/White_Slash_Thin/File2.png").convert_alpha()

    def __init__(self):
        self.sliced_points = []
        self.lines = []

        self.previous_mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        self.mouse_direction = pygame.Vector2(0, 0)
        self.angle = 0
        self.slicing = False
        self.display_image = self.IMAGE.copy()
        self.position = pygame.Vector2(0, 0)


    def update(self, delta):
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            pos = pygame.mouse.get_pos()
            self.sliced_points.append((pygame.Vector2(pos), pygame.time.get_ticks()))
            self.mouse_direction = pygame.Vector2(pos) - self.previous_mouse_pos
            self.previous_mouse_pos = pygame.Vector2(pos)
            if self.mouse_direction.x == 0:
                x_direction = self.mouse_direction.x + 0.0001
            else:
                x_direction = self.mouse_direction.x
            self.angle = math.degrees(math.atan(self.mouse_direction.y / x_direction))
            self.display_image, self.position = rotate_center(self.IMAGE, self.angle,
                                                              pygame.Vector2(pos) + pygame.Vector2(
                                                                  self.IMAGE.get_width() / 2, 0))
            self.slicing = True
        else:
            self.mouse_direction = pygame.Vector2(0, 0)
            self.previous_mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            self.angle = 0
            self.slicing = False

        self.lines.clear()
        if len(self.sliced_points) > 1:
            for i in range(len(self.sliced_points) - 1):
                self.lines.append((pygame.Vector2(self.sliced_points[i][0]), pygame.Vector2(self.sliced_points[i + 1][0])))

        for i, val in enumerate(self.sliced_points):
            pos, time = val
            if pygame.time.get_ticks() - time > self.LIFE_TIME:
                self.sliced_points.pop(i)
                break

    def hits(self, fruit):
        for line in self.lines:
            v1 = pygame.Vector2(line[0]) - fruit.position
            v2 = pygame.Vector2(line[1]) - fruit.position
            v = v2 - v1
            r = fruit.radius

            if v.magnitude_squared() == 0:
                continue

            discriminant = 4 * (v1.dot(v)) ** 2 - 4 * v.magnitude_squared() * (v1.magnitude_squared() - r ** 2)
            if discriminant >= 0:
                t1 = (-2 * v1.dot(v) + math.sqrt(discriminant)) / (2 * v.magnitude_squared())
                t2 = (-2 * v1.dot(v) - math.sqrt(discriminant)) / (2 * v.magnitude_squared())
                if 0 <= t1 <= 1 or 0 <= t2 <= 1:
                    return True
                if (t1 < 0 and t2 > 1) or (t2 < 0 and t1 > 1):
                    return True
        return False

    def draw(self, surf):
        # for line in self.lines:
        #     pygame.draw.circle(surf, BLUE, line[0], 5)
        #     # pygame.draw.rect(surf, RED, hitbox)
        #     pygame.draw.line(surf, GREEN, line[0], line[1], 4)
        #     mx, my = line[1] - line[0]
        #     if mx == 0:
        #         mx = 0.01
        #     m = my / mx
        #     c = line[0].y - m * line[0].x
        #
        #     x1 = line[0].x
        #     y1 = m * x1 + c
        #     x2 = line[1].x
        #     y2 = m * x2 + c
        #
        #     pygame.draw.line(surf, RED, (x1, y1), (x2, y2), 4)
        #     pygame.draw.rect(surf, RED, hitbox)
        #     pygame.draw.line(surf, RED, line[0], line[1], 4)
        # for pos, time in self.sliced_points:
        #     pygame.draw.circle(surf, RED, pos, 3)
        if len(self.sliced_points) > 1:
            pygame.draw.lines(surf, BLACK, False, [a for a, b in self.sliced_points], 6)
            pygame.draw.lines(surf, LIGHT_GRAY, False, [a for a, b in self.sliced_points], 4)
