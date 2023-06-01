import pygame

pygame.init()
WIDTH, HEIGHT = 800, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Fruit Ninja")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# commands
COMMAND_EXIT = 0
COMMAND_START = 1
