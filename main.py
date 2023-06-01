from setup import *


FPS = 120
clock = pygame.time.Clock()

is_running = True
while is_running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    screen.fill(WHITE)
    pygame.display.update()
pygame.quit()
