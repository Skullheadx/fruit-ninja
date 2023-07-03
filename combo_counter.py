from setup import *


class ComboCounter:
    LIFE_TIME = 1000

    def __init__(self, position, combo):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, -100)
        self.time = self.LIFE_TIME
        self.combo = f"x{combo}"
        self.text_surface = font_large.render(self.combo, True, DARK_GRAY)
        self.text_txt = Texture.from_surface(renderer, self.text_surface)

    def update(self, delta):
        self.position += self.velocity * delta / 1000
        self.time -= delta
        if self.time <= 0:
            return True

    def draw(self):
        self.text_txt.draw(None, self.position - pygame.Vector2(self.text_surface.get_width() / 2,
                                                                self.text_surface.get_height() / 2))
