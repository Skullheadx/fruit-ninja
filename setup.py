import pygame
from pygame._sdl2 import Window, Renderer, Texture, Image
import random
import os
import math
from functools import cache

pygame.init()
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
window = Window(size=(WIDTH,HEIGHT), fullscreen=True)
renderer = Renderer(window)
pygame.mouse.set_visible(False)

SCALE = pygame.Vector2(WIDTH / 1536, HEIGHT / 864)

pygame.display.set_caption("Fruit Shinobi")
icon = pygame.image.load("assets/logo.ico").convert()
pygame.display.set_icon(icon)

# fonts
font_small = pygame.font.Font("assets/font/go3v2.ttf", int(30 * SCALE.x))
font = pygame.font.Font("assets/font/go3v2.ttf", int(60 * SCALE.x))
font_large = pygame.font.Font("assets/font/go3v2.ttf", int(100 * SCALE.x))

# colors
WHITE = (255, 255, 255, 255)
LIGHT_GRAY = (211, 211, 211, 255)
GRAY = (128, 128, 128, 255)
DARK_GRAY = (25, 25, 25, 255)
BLACK = (0, 0, 0, 255)

RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
ORANGE = (255, 165, 0, 255)
YELLOW = (255, 255, 0, 255)
PURPLE = (128, 0, 128, 255)

BROWN = (139, 69, 19, 255)
DARK_BROWN = (119, 49, 0, 255)

DARK_RED = (139, 0, 0, 255)
DARK_GREEN = (0, 100, 0, 255)
DARK_BLUE = (0, 0, 139, 255)
DARK_ORANGE = (255, 140, 0, 255)
DARK_YELLOW = (255, 215, 0, 255)
DARK_PURPLE = (75, 0, 130, 255)

EFFECT_COLORS = [
    (252, 166, 168, 255),
    (247, 203, 168, 255),
    (203, 172, 239, 255),
    (160, 247, 208, 255),
    (222, 244, 141, 255),
    (205, 255, 135, 255),
    (174, 252, 201, 255),
    (247, 167, 111, 255),
    (225, 162, 239, 255),
    (209, 239, 119, 255),
    (211, 255, 178, 255),
    (119, 249, 215, 255),
    (252, 113, 146, 255),
    (204, 247, 160, 255),
    (247, 161, 148, 255),
    (218, 186, 255, 255),
    (112, 239, 116, 255),
    (237, 186, 125, 255),
    (198, 202, 255, 255),
    (197, 252, 174, 255),
]


def darken(color, factor=0.5):
    r, g, b, a = color
    return r * factor, g * factor, b * factor, a


def lighten(color, factor=0.5):
    r, g, b, a = color
    return min(255, r * (1 + factor)), min(255, g * (1 + factor)), min(255, b * (1 + factor)), a


# commands
COMMAND_EXIT = 0
COMMAND_START = 1
COMMAND_MENU = 2


def lerp(start, end, weight):
    return weight * (end - start) + start


def clamp(value, minimum, maximum):
    return min(maximum, max(minimum, value))

def determine_angle(pos1, pos2):
    pos1 = pygame.Vector2(pos1)
    pos2 = pygame.Vector2(pos2)
    if pos1.x == pos2.x:
        pos2.x += 0.0001
    a = math.degrees(math.atan((pos2.y - pos1.y) / (pos2.x - pos1.x)))
    return a
