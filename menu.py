import random

import pygame

from setup import *
from player import Player
from fruit import Fruit
from effect import SlashEffect, SplitEffect, BloodEffect, FadeOutEffect, BloodSplatter


class Menu:
    background = pygame.Surface((WIDTH, HEIGHT))
    tile_cols = 4
    tile_rows = 4
    background_tile = pygame.transform.scale(pygame.image.load("assets/background.png"),
                                             (WIDTH / tile_cols, HEIGHT / tile_rows)).convert()
    for x in range(tile_cols):
        for y in range(tile_rows):
            background.blit(background_tile, (x * WIDTH / tile_cols, y * HEIGHT / tile_rows))

    slash_sounds = [pygame.mixer.Sound(f"assets/sounds/Swishes/long-medium-swish-44324.wav"),
                    pygame.mixer.Sound(f"assets/sounds/Swishes/swing-6045.wav"),
                    pygame.mixer.Sound(f"assets/sounds/Swishes/swish-sound-94707.wav"),
                    ]

    def __init__(self):
        self.background_music = pygame.mixer.music.load(
            "assets/sounds/Of Far Different Nature - Ethnic Beat (CC-BY).ogg")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()

        self.player = Player()
        self.fruit = Fruit()
        self.fruit.position = pygame.Vector2(WIDTH / 2, HEIGHT * 1.5 / 2.5)
        self.fruit.angle = 0
        self.fruit.image = pygame.transform.scale(pygame.image.load("assets/fruits/58.png"),
                                                  (self.fruit.radius * 2, self.fruit.radius * 2))

        self.effects = []

        self.title_surface = font_large.render("Fruit Shinobi", True, WHITE)
        self.tutorial_surface = font.render("Drag to slice the fruit", True, WHITE)
        self.controls_surface = font_small.render("Press M to unmute music", True, WHITE)

        self.credit_surface = font_small.render("Made by: Skullheadx", True, WHITE)
        self.blacked_out = False

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.mixer.music.stop()
                return COMMAND_EXIT
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_m:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
        self.player.update(delta)

        if not self.blacked_out:
            hit_status = self.player.hits(self.fruit)
            if hit_status and SplitEffect.should_split(self.fruit.image, self.fruit.angle, self.fruit.position, self.player.previous_mouse_pos, self.player.mouse_direction):
                color = random.choice(COLORS)
                self.effects.append(BloodEffect(self.fruit.position, self.fruit.radius,lighten(color, 0.15)))

                half1, half2, pos1, pos2 = SplitEffect.split_image(self.fruit.image, self.fruit.angle, self.fruit.position, self.player.previous_mouse_pos,
                                                       self.player.mouse_direction)

                self.effects.append(BloodSplatter(self.fruit.position, self.fruit.radius,
                                                  determine_angle(self.fruit.position,
                                                                  self.fruit.position + self.player.mouse_direction),color))
                self.effects.append(SlashEffect(self.fruit.position, self.fruit.angle))

                n1, n2 = SplitEffect.find_normals(self.player.mouse_direction.normalize())
                c = 5
                self.effects.append(SplitEffect(pos1, half1, pygame.Vector2(0,0), n1 * c))
                self.effects.append(SplitEffect(pos2, half2, pygame.Vector2(0,0), n2 * c))

                pygame.mixer.Sound.play(random.choice(self.slash_sounds))
                self.blacked_out = True
                self.effects.append(FadeOutEffect())
        for effect in self.effects:
            effect_status = effect.update(delta)
            if effect_status:
                if isinstance(effect, FadeOutEffect):
                    return COMMAND_START
                self.effects.remove(effect)

    def draw(self, surf):
        surf.blit(self.background, (0, 0))
        if not self.blacked_out:
            self.fruit.draw(surf)

        tutorial_surface_pos = (
            WIDTH / 2, HEIGHT * 2 / 3 + self.tutorial_surface.get_height() / 2 + self.fruit.get_rect().height + 30)
        pygame.draw.rect(surf, DARK_GRAY, self.tutorial_surface.get_rect(center=tutorial_surface_pos).inflate(25, 25),
                         border_radius=10)
        pygame.draw.rect(surf, BLACK, self.tutorial_surface.get_rect(center=tutorial_surface_pos).inflate(25, 25), 5,
                         border_radius=10)
        surf.blit(self.tutorial_surface, self.tutorial_surface.get_rect(
            center=tutorial_surface_pos))

        pygame.draw.rect(surf, GRAY, self.title_surface.get_rect(center=(WIDTH / 2, HEIGHT / 3)).inflate(50, 50),
                         border_radius=10)
        pygame.draw.rect(surf, BLACK, self.title_surface.get_rect(center=(WIDTH / 2, HEIGHT / 3)).inflate(50, 50), 5,
                         border_radius=10)
        surf.blit(self.title_surface, self.title_surface.get_rect(center=(WIDTH / 2, HEIGHT / 3)))

        surf.blit(self.controls_surface, self.controls_surface.get_rect(bottomleft=(10, HEIGHT - 10)))
        surf.blit(self.credit_surface, self.credit_surface.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10)))
        self.player.draw(surf)
        for effect in self.effects:
            effect.draw(surf)
