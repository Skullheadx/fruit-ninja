# from game import Game
from menu import Menu
from setup import *


FPS = 60
clock = pygame.time.Clock()

scene = Menu()

is_running = True
while is_running:
    delta = clock.tick(FPS)
    renderer.clear()


    status = scene.update(delta)
    scene.draw()

    fps_text = font.render(f"FPS {int(clock.get_fps())}", True, WHITE)
    fps_text_txt = Texture.from_surface(renderer, fps_text)
    fps_text_txt.draw(None, (WIDTH - fps_text.get_width() - 7, 0))

    renderer.present()

    if status == COMMAND_EXIT:
        is_running = False
    # elif status == COMMAND_START:
    #     scene = Game()
    # elif status == COMMAND_MENU:
    #     scene = Menu()

pygame.quit()
