from setup import *
from player import Player
from fruit import Fruit
from effect import SlashEffect, SplitEffect, BloodEffect, FadeOutEffect, BloodSplatter
from rect import Rect


class Menu:
    # Creating background image
    background = pygame.Surface((WIDTH, HEIGHT))
    tile_cols = 4
    tile_rows = 4
    background_tile = pygame.transform.scale(pygame.image.load("assets/background.png"),
                                             (WIDTH / tile_cols, HEIGHT / tile_rows)).convert()
    for x in range(tile_cols):
        for y in range(tile_rows):
            background.blit(background_tile, (x * WIDTH / tile_cols, y * HEIGHT / tile_rows))
    bg_txt = Texture.from_surface(renderer, background)

    # Slash sound effects
    slash_sounds = [
        pygame.mixer.Sound(f"assets/sounds/Swishes/long-medium-swish-44324.ogg"),
        pygame.mixer.Sound(f"assets/sounds/Swishes/swing-6045.ogg"),
        pygame.mixer.Sound(f"assets/sounds/Swishes/swish-sound-94707.ogg"),
    ]

    def __init__(self):
        # Music
        pygame.mixer.music.load("assets/sounds/Of Far Different Nature - Ethnic Beat (CC-BY).ogg")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()

        # Player
        self.player = Player()

        # Fruit
        self.fruit = Fruit()
        self.fruit.position = pygame.Vector2(WIDTH / 2, HEIGHT * 1.5 / 2.5)
        self.fruit.angle = 0
        self.fruit.image = pygame.image.load("assets/fruits/58.png")
        self.fruit.fruit_txt = Texture.from_surface(renderer, self.fruit.image)

        # Effects
        self.effects = []

        # Text surfaces
        self.title_surface = font_large.render("Fruit Shinobi", True, WHITE)
        self.tutorial_surface = font.render("Drag to slice the fruit", True, WHITE)
        self.controls_surface = font_small.render("Press M to unmute music", True, WHITE)
        self.credit_surface = font_small.render("Made by: Skullheadx", True, WHITE)

        self.title_txt = Texture.from_surface(renderer, self.title_surface)
        self.tutorial_txt = Texture.from_surface(renderer, self.tutorial_surface)
        self.controls_txt = Texture.from_surface(renderer, self.controls_surface)
        self.credit_txt = Texture.from_surface(renderer, self.credit_surface)

        # Rect textures
        self.tutorial_surface_pos = (
            WIDTH / 2, HEIGHT * 2 / 3 + self.tutorial_surface.get_height() / 2 + self.fruit.radius + 30)

        self.r1 = Rect(self.tutorial_surface.get_rect(center=self.tutorial_surface_pos).inflate(25, 25), DARK_GRAY, 10)
        self.r2 = Rect(self.tutorial_surface.get_rect(center=self.tutorial_surface_pos).inflate(25, 25), BLACK, 10, 5)

        self.r3 = Rect(self.title_surface.get_rect(center=(WIDTH / 2, HEIGHT / 3)).inflate(50, 50), GRAY, 10)
        self.r4 = Rect(self.title_surface.get_rect(center=(WIDTH / 2, HEIGHT / 3)).inflate(50, 50), BLACK, 10, 5)

        # blacked out
        self.blacked_out = False

    def update(self, delta):
        # Event handling
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

        # Update player
        self.player.update(delta)

        # Update fruit
        if not self.blacked_out:
            hit_status = self.player.hits(self.fruit)  # Check if player hits fruit
            # Check if fruit should split
            if hit_status and SplitEffect.should_split(self.fruit.fruit_txt, self.fruit.angle, self.fruit.position,
                                                       self.player.previous_mouse_pos, self.player.mouse_direction,
                                                       self.fruit.radius):
                # Split fruit
                color = random.choice(EFFECT_COLORS)
                n1, n2 = SplitEffect.find_normals(self.player.mouse_direction.normalize() * 5)

                self.effects.append(BloodSplatter(self.fruit.position, self.fruit.radius,
                                                  determine_angle(self.fruit.position,
                                                                  self.fruit.position + self.player.mouse_direction),
                                                  color))
                self.effects.append(BloodEffect(self.fruit.position, self.fruit.radius, lighten(color, 0.15)))
                half1, half2, pos1, pos2 = SplitEffect.split_image(self.fruit.fruit_txt, self.fruit.angle,
                                                                   self.fruit.position, self.player.previous_mouse_pos,
                                                                   self.player.mouse_direction, self.fruit.radius)

                self.effects.append(SplitEffect(pos1, half1, pygame.Vector2(0, 0), n1))
                self.effects.append(SplitEffect(pos2, half2, pygame.Vector2(0, 0), n2))
                self.effects.append(SlashEffect(self.fruit.position, self.fruit.angle))

                # Play slash sound
                pygame.mixer.Sound.play(random.choice(self.slash_sounds))

                # cue fadeout
                self.blacked_out = True
                self.effects.append(FadeOutEffect())

        # Update effects
        for effect in self.effects:
            effect_status = effect.update(delta)
            if effect_status:
                if isinstance(effect, FadeOutEffect):
                    return COMMAND_START
                self.effects.remove(effect)

    def draw(self):
        self.bg_txt.draw(None, (0, 0))

        if not self.blacked_out:
            self.fruit.draw()

        self.r1.draw()
        self.r2.draw()

        self.tutorial_txt.draw(None, self.tutorial_surface.get_rect(
            center=self.tutorial_surface_pos))

        self.r3.draw()
        self.r4.draw()

        self.title_txt.draw(None, self.title_surface.get_rect(center=(WIDTH / 2, HEIGHT / 3)))

        self.controls_txt.draw(None, self.controls_surface.get_rect(bottomleft=(10, HEIGHT - 10)))
        self.credit_txt.draw(None, self.credit_surface.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10)))


        for effect in self.effects:
            effect.draw()
        self.player.draw()
