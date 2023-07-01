import pygame
import random
import os
import math
from functools import cache

pygame.init()
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

SCALE = pygame.Vector2(WIDTH / 1536, HEIGHT / 864)

pygame.display.set_caption("Fruit Shinobi")
icon = pygame.image.load("assets/logo.ico").convert()
pygame.display.set_icon(icon)

# fonts
font_small = pygame.font.Font("assets/font/go3v2.ttf", int(30 * SCALE.x))
font = pygame.font.Font("assets/font/go3v2.ttf", int(60 * SCALE.x))
font_large = pygame.font.Font("assets/font/go3v2.ttf", int(100 * SCALE.x))

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
DARK_BROWN = (119, 49, 0)

DARK_RED = (139, 0, 0)
DARK_GREEN = (0, 100, 0)
DARK_BLUE = (0, 0, 139)
DARK_ORANGE = (255, 140, 0)
DARK_YELLOW = (255, 215, 0)
DARK_PURPLE = (75, 0, 130)

DEFAULT_COLORS = [
    RED,
    GREEN,
    BLUE,
    ORANGE,
    YELLOW,
    PURPLE,
    DARK_RED,
    DARK_GREEN,
    DARK_BLUE,
    DARK_ORANGE,
    DARK_YELLOW,
    DARK_PURPLE
]

COLORS = [
    (252, 166, 168),
    (247, 203, 168),
    (203, 172, 239),
    (160, 247, 208),
    (222, 244, 141),
    (205, 255, 135),
    (174, 252, 201),
    (247, 167, 111),
    (225, 162, 239),
    (209, 239, 119),
    (211, 255, 178),
    (119, 249, 215),
    (252, 113, 146),
    (204, 247, 160),
    (247, 161, 148),
    (218, 186, 255),
    (112, 239, 116),
    (237, 186, 125),
    (198, 202, 255),
    (197, 252, 174),
]


def darken(color, factor=0.5):
    r, g, b = color
    return (r * factor, g * factor, b * factor)


def lighten(color, factor=0.5):
    r, g, b = color
    return (min(255, r * (1 + factor)), min(255, g * (1 + factor)), min(255, b * (1 + factor)))


# commands
COMMAND_EXIT = 0
COMMAND_START = 1
COMMAND_MENU = 2

screen.fill(BROWN)
loading_text = font_large.render("Loading...", True, BLACK)
screen.blit(loading_text, loading_text.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
pygame.display.update()


def lerp(start, end, weight):
    return weight * (end - start) + start


def clamp(value, minimum, maximum):
    return min(maximum, max(minimum, value))


@cache
def rotate(image, angle):
    return pygame.transform.rotate(image, angle)


def rotate_center(image, angle, position):
    rotated_image = rotate(image, round(angle))
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=(
        position.x - image.get_rect().width / 2, position.y - image.get_rect().height / 2)).center)
    return rotated_image, new_rect.topleft


def determine_angle(pos1, pos2):
    pos1 = pygame.Vector2(pos1)
    pos2 = pygame.Vector2(pos2)

    if pos1.x == pos2.x:
        pos2.x += 0.0001

    a = math.degrees(math.atan((pos2.y - pos1.y) / (pos2.x - pos1.x)))

    # if pos2.x < pos1.x:
    #     a += 180
    return -a

# def split_image(image, angle, image_position, mouse_position, mouse_direction):
#     img = image.copy()
#     ip = pygame.Vector2(img.get_width() / 2, img.get_height() / 2)
#     mp = mouse_position - ip
#
#     if mouse_direction.x == 0:
#         a = 90
#     else:
#         a = math.degrees(math.atan(mouse_direction.y/mouse_direction.x))
#
#     mp.rotate_ip(-a)
#     mp += ip
#
#     pygame.draw.line(img, RED,mouse_position-image_position, mouse_direction * 100+ mouse_position-image_position, 20)
#
#     rot_img,pos = rotate_center(img, -a, image_position)
#     return img, rot_img, (WIDTH/2, HEIGHT/2), (0,0)
#     crop_y = clamp(int(mp.y), 0, img.get_height())
#
#     half1 = pygame.transform.rotate(img2.subsurface((0, 0, img.get_width(), crop_y)), a)
#     half2 = pygame.transform.rotate(img2.subsurface((0, crop_y, img.get_width(), img.get_height() - crop_y)), a)
#     #
#     # return half1, half2, half1.get_rect(topleft=pos1).center, half2.get_rect(topleft=pos2).center

# good one :D
# def split_image(image, angle, image_position, mouse_position, mouse_direction):
#     img = image.copy()
#
#     if mouse_direction.x == 0:
#         mouse_direction.x += 0.0001
#
#     a = math.degrees(math.atan(mouse_direction.y / mouse_direction.x))
#
#     img = rotate_center(img, a, pygame.Vector2(0, 0))[0]
#
#     top_left = pygame.Vector2(image_position) - pygame.Vector2(img.get_width() / 2, img.get_height() / 2)
#     rot_center = pygame.Vector2(image_position) - top_left
#
#     # finding end and start points of the splitting line
#     # [x,y] = mouse_position + t * mouse_direction # vector equation
#     # x = mouse_position.x + t * mouse_direction.x
#     # y = mouse_position.y + t * mouse_direction.y
#
#     mp = mouse_position - top_left
#
#     t1 = (- mp.x) / mouse_direction.x
#     p1 = mp + t1 * mouse_direction
#
#     t2 = (img.get_width() - mp.x) / mouse_direction.x
#     p2 = mp + t2 * mouse_direction
#
#     p3 = (p1 - rot_center).rotate(-a) + rot_center
#     p4 = (p2-rot_center).rotate(-a) + rot_center
#
#     half1 = img.subsurface(pygame.Rect(0, 0, img.get_width(), clamp(p3.y,0, img.get_height())))
#     half2 = img.subsurface(pygame.Rect(0, clamp(p3.y,0, img.get_height()), img.get_width(), clamp(img.get_height() - p3.y, 0, img.get_height())))
#
#     p5 = half1.get_rect().center - rot_center
#     pos1 = (p5).rotate(a) + image_position
#
#     p6 = half2.get_rect().center - rot_center + pygame.Vector2(0, clamp(p3.y,0, img.get_height()))
#     pos2 = (p6).rotate(a) + image_position
#
#     r_half1 = pygame.transform.rotate(half1, -a)
#     r_half2 = pygame.transform.rotate(half2, -a)
#
#     return r_half1, r_half2, pos1, pos2


# def split_image(image, angle, pos1, pos2, image_position):
#     pos1 = pygame.Vector2(pos1) - image_position + pygame.Vector2(image.get_width() / 2, image.get_height() / 2)
#     pos2 = pygame.Vector2(pos2) - image_position + pygame.Vector2(image.get_width() / 2, image.get_height() / 2)
#
#     if pos1.x == pos2.x:
#         pos2.x += 0.0001
#
#     img = image.copy()
#
#     center = pygame.Vector2(img.get_width() / 2, img.get_height() / 2)
#
#     # pygame.draw.circle(img, BLACK, center, 5)
#     # pygame.draw.circle(img, RED, pos1, 15)
#     # pygame.draw.circle(img, GREEN, pos2, 15)
#     # pygame.draw.line(img, BLACK, pos1, pos2, 5)
#
#     a = math.degrees(math.atan((pos2.y - pos1.y) / (pos2.x - pos1.x)))
#     img = rotate_center(img, a, pygame.Vector2(0, 0))[0]
#     p1 = (pos1 - center).rotate(-a) + img.get_rect().center
#     p2 = (pos2 - center).rotate(-a) + img.get_rect().center
#
#     # pygame.draw.circle(img, BLACK, center, 5)
#     # pygame.draw.circle(img, BLUE, p1, 15)
#     # pygame.draw.circle(img, WHITE, p2, 15)
#
#     rot_center = pygame.Vector2(img.get_width() / 2, img.get_height() / 2)
#     p3 = (-rot_center.copy()).rotate(-a) + center
#     p4 = pygame.Vector2(-image.get_width() / 2, 0).rotate(-a) + center
#
#     half1 = pygame.transform.rotate(img.subsurface(pygame.Rect(0, 0, img.get_width(), min(p1.y, img.get_height()))),
#                                     -a).convert_alpha()
#     half2 = pygame.transform.rotate(
#         img.subsurface(pygame.Rect(0, min(p1.y, img.get_height()), img.get_width(), max(img.get_height() - p1.y, 0))),
#         -a).convert_alpha()
#     #
#     if 0 < a < 90:
#         p3, p4 = p4, p3
#
#     half1, pos1 = rotate_center(half1, angle,
#                                 p3 + image_position + pygame.Vector2(half1.get_width() / 2, half1.get_height() / 2))
#     half2, pos2 = rotate_center(half2, angle,
#                                 p4 + image_position + pygame.Vector2(half2.get_width() / 2, half2.get_height() / 2))
#
#     return half1, half2, pos1, pos2
