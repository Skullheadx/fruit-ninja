import pygame
from pygame._sdl2 import Window, Renderer, Texture

class App:

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((1366, 768))
        self.window = Window.from_display_module()
        self.renderer = Renderer(self.window)
        self.renderer.draw_color = (255, 0, 0, 255)

        a_surface = pygame.image.load('image.png')
        self.an_image = Texture.from_surface(self.renderer, a_surface)

    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            self.renderer.clear()
            self.an_image.draw(None, (20, 20))
            self.renderer.present()
            self.clock.tick(60)


app = App()
app.run()