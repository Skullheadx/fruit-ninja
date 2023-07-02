from setup import *


def get_rect_txt(rect, color, border_radius, thickness=0):
    r = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(r, color, (0, 0, rect.width, rect.height), border_radius=border_radius,
                     width=thickness)
    return Texture.from_surface(renderer, r)


class Rect:

    def __init__(self, rect, color, border_radius=0, thickness=0):
        self.position = pygame.Vector2(rect.x, rect.y)
        self.texture = get_rect_txt(rect, color, border_radius, thickness)

    def draw(self):
        self.texture.draw(None, self.position)
