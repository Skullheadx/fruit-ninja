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
    screen.blit(font.render(f"FPS: {clock.get_fps():.2f}", True, BLACK), (0, 0))
    pygame.display.update()

    if status == COMMAND_EXIT:
        is_running = False
    elif status == COMMAND_START:
        scene = Game()


pygame.quit()
