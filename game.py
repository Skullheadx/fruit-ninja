import pygame

from bomb import Bomb
from combo_counter import ComboCounter
from effect import BloodEffect, SplitEffect, SlashEffect, FadeInEffect, FadeOutEffect, BloodSplatter
from fruit import Fruit
from player import Player
from setup import *


class Game:
    BOMB_CHANCE = 0
    EFFECT_COUNT_PER_FRUIT = 20
    EFFECT_COUNT_PER_BOMB = 0
    COMBO_TIME = 250
    GAME_OVER_TIME = 2000
    WAVE_COOLDOWN = 500

    BACKGROUND = pygame.Surface((WIDTH, HEIGHT))
    tile_cols = 4
    tile_rows = 4
    background_tile = pygame.transform.scale(pygame.image.load("assets/background.png"),
                                             (WIDTH / tile_cols, HEIGHT / tile_rows)).convert()
    dark_background_tile = pygame.transform.scale(pygame.image.load("assets/dark_background.png"),
                                                  (WIDTH / tile_cols, HEIGHT / tile_rows)).convert()
    for x in range(tile_cols):
        for y in range(tile_rows):
            if y == 0:
                BACKGROUND.blit(dark_background_tile, (x * WIDTH / tile_cols, y * HEIGHT / tile_rows))
            else:
                BACKGROUND.blit(background_tile, (x * WIDTH / tile_cols, y * HEIGHT / tile_rows))
    bass_sound_effect = pygame.mixer.Sound("assets/sounds/sub-bass-4-secondsssss-6241.wav")
    bass_sound_effect.set_volume(0.1)
    slash_sounds = [pygame.mixer.Sound(f"assets/sounds/Swishes/long-medium-swish-44324.wav"),
                    pygame.mixer.Sound(f"assets/sounds/Swishes/swing-6045.wav"),
                    pygame.mixer.Sound(f"assets/sounds/Swishes/swish-sound-94707.wav"),
                    ]

    HIGHSCORE_FILE = "highscore.txt"

    def __init__(self):
        self.player = Player()
        self.fruits = [Fruit()]
        self.bombs = []
        self.effects = [
            [], # Blood splatter
            [], # Blood splash
            [], # Split Effect
            [], # slash effect
            [FadeInEffect(fade_time=1000)] # Fade in/fade out effects
        ]
        self.combo_counters = []
        self.wave = 10
        self.score = 0
        self.time_since_last_hit = 0
        self.current_combo = 0

        self.cleared_wave = True
        self.wave_cooldown_timer = 0

        self.game_over = False
        self.game_over_time = 0

        try:
            with open(self.HIGHSCORE_FILE, "r") as f:
                self.highscore = int(f.read())
        except:
            self.highscore = 0

        self.music_started = False
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(500)
            background_music = pygame.mixer.music.load(
                "assets/sounds/Of Far Different Nature - Friendly Trap (CC-BY).ogg")
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1)
            self.music_started = True

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return COMMAND_EXIT
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return COMMAND_EXIT
                elif event.key == pygame.K_m:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                        if not self.music_started:
                            background_music = pygame.mixer.music.load(
                                "assets/sounds/Of Far Different Nature - Friendly Trap (CC-BY).ogg")
                            pygame.mixer.music.set_volume(0.25)
                            pygame.mixer.music.play(-1)
                            self.music_started = True
        if not self.game_over:
            self.player.update(delta)
        else:
            self.game_over_time += delta
            if self.game_over_time > self.GAME_OVER_TIME:
                return COMMAND_START
        hits = []

        for fruit in self.fruits:
            fruit.update(delta)
            hit_status = self.player.hits(fruit)
            if hit_status and SplitEffect.should_split(fruit.image, fruit.angle, fruit.position, self.player.previous_mouse_pos, self.player.mouse_direction):
                hits.append((fruit, self.player.mouse_direction, self.player.previous_mouse_pos))

            fr = fruit.get_rect()
            if ((not -fruit.width < fr.x < WIDTH + fruit.width) or fr.y - fr.height > HEIGHT) and fruit.velocity.y > 0:
                self.fruits.remove(fruit)
                self.cleared_wave = False
        self.time_since_last_hit += delta

        if self.time_since_last_hit < self.COMBO_TIME:
            self.score += self.current_combo
        else:
            self.current_combo = 0

        for hit, mouse_direction, mouse_position in hits:

            color = random.choice(COLORS)
            self.effects[0].append(
                BloodSplatter(hit.position, hit.radius, determine_angle(hit.position, hit.position + mouse_direction),color))
            self.effects[1].append(BloodEffect(hit.position, hit.radius,lighten(color, 0.15)))

            half1, half2, pos1, pos2 = SplitEffect.split_image(hit.image, hit.angle, hit.position, mouse_position, mouse_direction)

            n1, n2 = SplitEffect.find_normals(mouse_direction.normalize())
            c = 100
            self.effects[2].append(SplitEffect(pos1, half1, hit.velocity, n1 * c))
            self.effects[2].append(SplitEffect(pos2, half2, hit.velocity, n2 * c))

            pygame.mixer.Sound.play(random.choice(self.slash_sounds))

            self.score += 1
            if self.time_since_last_hit < self.COMBO_TIME:
                self.current_combo += 1
            if self.current_combo > 1:
                self.combo_counters.append(ComboCounter(hit.position, f"x{self.current_combo + 1}"))
                self.effects[3].append(SlashEffect(hit.position, hit.angle, combo=False))
            else:
                self.effects[3].append(SlashEffect(hit.position, hit.angle))

            self.time_since_last_hit = 0

            if hit in self.fruits:
                self.fruits.remove(hit)

        for layer in self.effects:
            for effect in layer:
                effect_status = effect.update(delta)
                if effect_status:
                    layer.remove(effect)
        for combo in self.combo_counters:
            combo_status = combo.update(delta)
            if combo_status:
                self.combo_counters.remove(combo)

        for bomb in self.bombs:
            bomb_status = bomb.update(delta)

            if self.player.hits(bomb):
                bomb.explode(self.fruits, self.bombs, self.effects[2])
                self.game_over = True
                self.player.sliced_points.clear()
                pygame.mixer.Sound.play(self.bass_sound_effect)
                self.effects[4].append(FadeOutEffect(fade_time=self.GAME_OVER_TIME, max_alpha=20))
                if self.score > self.highscore:
                    self.highscore = self.score
                    with open(self.HIGHSCORE_FILE, "w") as f:
                        f.write(str(self.highscore))
            if bomb_status:
                self.bombs.remove(bomb)
                continue
            br = bomb.get_rect()
            if ((not -bomb.width < br.x < WIDTH + bomb.width) or br.y - br.height > HEIGHT) and bomb.velocity.y > 0:
                self.bombs.remove(bomb)

        if len(self.fruits) == 0 and len(self.bombs) == 0 and not self.game_over:
            self.wave_cooldown_timer += delta
            if self.wave_cooldown_timer >= self.WAVE_COOLDOWN:
                if self.cleared_wave:
                    self.wave_cooldown_timer = 0
                    self.wave += 1
                self.cleared_wave = True
                for i in range(self.wave):
                    if random.random() < self.BOMB_CHANCE:
                        self.bombs.append(Bomb())
                    else:
                        self.fruits.append(Fruit())

    def draw(self, surf):

        screen.blit(self.BACKGROUND, (0, 0))

        text_surf = font.render(f"SCORE {self.score}", True, WHITE)
        surf.blit(text_surf, (7, 0))
        text_surf2 = font.render(f"COMBO x{max(1, self.current_combo)}", True, WHITE)
        surf.blit(text_surf2, text_surf2.get_rect(center=(WIDTH / 2, text_surf.get_height() / 2)))
        # text_surf2 = font.render(f"TIME SINCE LAST HIT {round(self.time_since_last_hit / 1000, 1)}", True, BLACK)
        # surf.blit(text_surf2, (WIDTH - text_surf2.get_width(), text_surf.get_height()))

        for effect in self.effects[0]:
            effect.draw(surf)
        for effect in self.effects[1]:
            effect.draw(surf)
        for bomb in self.bombs:
            bomb.draw(surf)
        for effect in self.effects[2]:
            effect.draw(surf)
        for fruit in self.fruits:
            fruit.draw(surf)
        for effect in self.effects[3]:
            effect.draw(surf)
        for combo in self.combo_counters:
            combo.draw(surf)
        self.player.draw(surf)
        for effect in self.effects[4]:
            effect.draw(surf)
        if self.game_over:
            title = font_large.render("GAME OVER", True, WHITE)
            subtitle = font.render(f"HIGHSCORE {self.highscore}", True, WHITE)
            game_over_surf = pygame.Surface(
                (max(title.get_width(), subtitle.get_width()), title.get_height() + subtitle.get_height()))
            game_over_surf.fill(GRAY)
            game_over_surf.blit(title, title.get_rect(center=(game_over_surf.get_width() / 2, title.get_height() / 2)))
            game_over_surf.blit(subtitle, subtitle.get_rect(
                center=(game_over_surf.get_width() / 2, title.get_height() + subtitle.get_height() / 2)))

            pygame.draw.rect(surf, GRAY, game_over_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2)).inflate(50, 50),
                             border_radius=10)
            pygame.draw.rect(surf, BLACK, game_over_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2)).inflate(50, 50), 5,
                             border_radius=10)
            surf.blit(game_over_surf, game_over_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2)))