from game import Game
from menu import Menu
from setup import *

FPS = 60
clock = pygame.time.Clock()

scene = Menu()

is_running = True
while is_running:
    delta = clock.tick(FPS)
    status = scene.update(delta)
    scene.draw(screen)
    fps_text = font.render(f"FPS {int(clock.get_fps())}", True, WHITE)
    screen.blit(fps_text, (WIDTH - fps_text.get_width() - 7, 0))

    pygame.display.update()

    if status == COMMAND_EXIT:
        is_running = False
    elif status == COMMAND_START:
        scene = Game()
    elif status == COMMAND_MENU:
        scene = Menu()

pygame.quit()
