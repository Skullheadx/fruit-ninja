import pygame
import random

pygame.init()
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

pygame.display.set_caption("Fruit Ninja")

# colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (211, 211, 211)
GRAY = (128, 128, 128)
DARK_GRAY = (25, 25, 25)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

BROWN = (139, 69, 19)

DARK_RED = (139, 0, 0)
DARK_GREEN = (0, 100, 0)
DARK_BLUE = (0, 0, 139)
DARK_ORANGE = (255, 140, 0)
DARK_YELLOW = (255, 215, 0)
DARK_PURPLE = (75, 0, 130)
DARKEN = {RED: DARK_RED, ORANGE: DARK_ORANGE, YELLOW: DARK_YELLOW, GREEN: DARK_GREEN, BLUE: DARK_BLUE,
          PURPLE: DARK_PURPLE}
LIGHTEN = {RED: ORANGE, ORANGE: YELLOW, YELLOW: GREEN, GREEN: BLUE, BLUE: PURPLE, PURPLE: RED}

# commands
COMMAND_EXIT = 0
COMMAND_START = 1


def lerp(start, end, weight):
    return weight * (end - start) + start


font = pygame.font.SysFont("Arial", 50)
