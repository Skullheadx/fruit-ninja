import pygame.mouse

from setup import *


class Player:
    LIFE_TIME = 100

    image = pygame.image.load("assets/knife.png").convert_alpha()
    txt = Texture.from_surface(renderer, image)

    SIZE = pygame.Vector2(50* SCALE, 50* SCALE)

    def __init__(self):
        self.sliced_points = []
        self.lines = []

        self.previous_mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        self.mouse_direction = pygame.Vector2(0, 0)
        self.slicing = False

        self.angle = 0

    def update(self, delta):
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            pos = pygame.mouse.get_pos()
            self.sliced_points.append((pygame.Vector2(pos), pygame.time.get_ticks()))
            self.mouse_direction = pygame.Vector2(pos) - self.previous_mouse_pos
            self.previous_mouse_pos = pygame.Vector2(pos)
            self.slicing = True
        else:
            self.mouse_direction = pygame.Vector2(0, 0)
            self.previous_mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            self.slicing = False


        self.lines.clear()
        if len(self.sliced_points) > 1:
            for i in range(len(self.sliced_points) - 1):
                self.lines.append(
                    (pygame.Vector2(self.sliced_points[i][0]), pygame.Vector2(self.sliced_points[i + 1][0])))

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

    def draw(self):
        renderer.draw_color = LIGHT_GRAY
        if len(self.sliced_points) > 1:
            for i in range(len(self.sliced_points) - 1):
                renderer.draw_line(self.sliced_points[i][0], self.sliced_points[i + 1][0])
        renderer.draw_line(self.previous_mouse_pos, self.previous_mouse_pos - self.mouse_direction)
        self.txt.draw(None, pygame.Rect(pygame.mouse.get_pos(), self.SIZE))

