import asyncio
import pygame
from pygame._sdl2 import Window, Renderer, Texture, Image
import random
import os
import math
from setup import *
from game import Game
from menu import Menu


async def main():
    FPS = 60
    clock = pygame.time.Clock()

    scene = Menu()
    is_running = True
    while is_running:
        delta = clock.tick(FPS)
        renderer.clear()

        status = scene.update(delta)
        scene.draw()

        # fps_text = font_small.render(f"FPS: {clock.get_fps():.0f}", True, DARK_GRAY)
        # fps_txt = Texture.from_surface(renderer, fps_text)
        # fps_txt.draw(None, pygame.Vector2(10, 75))

        renderer.present()
        await asyncio.sleep(0)

        if status == COMMAND_EXIT:
            is_running = False
        elif status == COMMAND_START:
            scene = Game()
        elif status == COMMAND_MENU:
            scene = Menu()

    pygame.quit()

asyncio.run(main())
