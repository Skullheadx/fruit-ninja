from setup import *
from game import Game

FPS = 120
clock = pygame.time.Clock()

scene = Game()

is_running = True
while is_running:
    delta = clock.tick(FPS)
    status = scene.update(delta)
    scene.draw(screen)
    pygame.display.update()

    if status == COMMAND_EXIT:
        is_running = False

pygame.quit()
