from player import Player
from fruit import Fruit
from effect import BloodEffect, SplitEffect, SlashEffect, FadeInEffect, FadeOutEffect, BloodSplatter
from combo_counter import ComboCounter
from bomb import Bomb
from rect import Rect
from setup import *


class Game:
    BOMB_CHANCE = 0.1

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
    BACKGROUND = Texture.from_surface(renderer, BACKGROUND)

    bass_sound_effect = pygame.mixer.Sound("assets/sounds/sub-bass-4-secondsssss-6241.wav")
    bass_sound_effect.set_volume(0.1)
    slash_sounds = [pygame.mixer.Sound(f"assets/sounds/Swishes/long-medium-swish-44324.wav"),
                    pygame.mixer.Sound(f"assets/sounds/Swishes/swing-6045.wav"),
                    pygame.mixer.Sound(f"assets/sounds/Swishes/swish-sound-94707.wav"),
                    ]

    HIGH_SCORE_FILE = "high_score.txt"

    def __init__(self):
        self.player = Player()

        self.fruits = [Fruit()]
        self.bombs = []

        self.effects = [
            [],  # Blood splatter
            [],  # Blood splash
            [],  # Split Effect
            [],  # slash effect
            [FadeInEffect(fade_time=1000)]  # Fade in/fade out effects
        ]

        self.combo_counters = []

        self.score = 0

        self.time_since_last_hit = 0
        self.current_combo = 0

        self.wave = 1
        self.cleared_wave = True
        self.wave_cooldown_timer = 0

        self.game_over = False
        self.game_over_time = 0

        try:
            with open(self.HIGH_SCORE_FILE, "r") as f:
                self.high_score = int(f.read())
        except:
            self.high_score = 0

        self.music_started = False
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.load("assets/sounds/Of Far Different Nature - Friendly Trap (CC-BY).ogg")
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1)
            self.music_started = True

        self.score_surf = font.render(f"SCORE {self.score}", True, WHITE)
        self.score_txt = Texture.from_surface(renderer, self.score_surf)

        self.combo_surf = font.render(f"COMBO x{max(1,self.current_combo)}", True, WHITE)
        self.combo_txt = Texture.from_surface(renderer, self.combo_surf)

        self.high_score_surf = font.render(f"BEST {self.high_score}", True, WHITE)
        self.high_score_txt = Texture.from_surface(renderer, self.high_score_surf)

        self.title_surf = font_large.render("GAME OVER", True, WHITE)

        self.subtitle_surf = font.render(f"HIGH SCORE {self.high_score}", True, WHITE)

        self.game_over_surf = pygame.Surface((max(self.title_surf.get_width(), self.subtitle_surf.get_width()),
                                              self.title_surf.get_height() + self.subtitle_surf.get_height()))
        self.game_over_surf.fill(GRAY)
        self.game_over_surf.blit(self.title_surf, self.title_surf.get_rect(
            center=(self.game_over_surf.get_width() / 2, self.title_surf.get_height() / 2)))
        self.game_over_surf.blit(self.subtitle_surf, self.subtitle_surf.get_rect(
            center=(
                self.game_over_surf.get_width() / 2,
                self.title_surf.get_height() + self.subtitle_surf.get_height() / 2)))
        self.game_over_txt = Texture.from_surface(renderer, self.game_over_surf)

        self.r1 = Rect(self.game_over_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2)).inflate(50, 50), GRAY, 10)
        self.r2 = Rect(self.game_over_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2)).inflate(50, 50), BLACK, 10, 5)

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                if self.score > self.high_score:
                    self.high_score = self.score
                    with open(self.HIGH_SCORE_FILE, "w") as f:
                        f.write(str(self.high_score))
                return COMMAND_EXIT
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_m:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                        if not self.music_started:
                            pygame.mixer.music.load("assets/sounds/Of Far Different Nature - Friendly Trap (CC-BY).ogg")
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
            if hit_status and SplitEffect.should_split(fruit.fruit_txt, fruit.angle, fruit.position,
                                                       self.player.previous_mouse_pos,
                                                       self.player.mouse_direction, fruit.radius):
                hits.append((fruit, self.player.mouse_direction, self.player.previous_mouse_pos))

            if (((not -fruit.radius * 2 < fruit.position.x < WIDTH + fruit.radius * 2) or
                 fruit.position.y - fruit.radius * 2 > HEIGHT) and fruit.velocity.y > 0):
                self.fruits.remove(fruit)
                self.cleared_wave = False

        self.time_since_last_hit += delta

        if self.time_since_last_hit < self.COMBO_TIME:
            self.score += self.current_combo
            self.score_surf = font.render(f"SCORE {self.score}", True, WHITE)
            self.score_txt = Texture.from_surface(renderer, self.score_surf)
            self.high_score_surf = font.render(f"BEST {self.high_score}", True, WHITE)
            self.high_score_txt = Texture.from_surface(renderer, self.high_score_surf)
        else:
            self.current_combo = 0
            self.combo_surf = font.render(f"COMBO x{max(1,self.current_combo)}", True, WHITE)
            self.combo_txt = Texture.from_surface(renderer, self.combo_surf)

        for hit, mouse_direction, mouse_position in hits:
            color = random.choice(EFFECT_COLORS)
            self.effects[0].append(BloodSplatter(hit.position, hit.radius,
                                                 determine_angle(hit.position, hit.position + mouse_direction),
                                                 color))
            self.effects[1].append(BloodEffect(hit.position, hit.radius, lighten(color, 0.15)))

            half1, half2, pos1, pos2 = SplitEffect.split_image(hit.fruit_txt, hit.angle, hit.position, mouse_position,
                                                               mouse_direction, hit.radius)

            n1, n2 = SplitEffect.find_normals(mouse_direction.normalize() * 5)
            self.effects[2].append(SplitEffect(pos1, half1, hit.velocity, n1))
            self.effects[2].append(SplitEffect(pos2, half2, hit.velocity, n2))

            pygame.mixer.Sound.play(random.choice(self.slash_sounds))

            self.score += 1
            self.score_surf = font.render(f"SCORE {self.score}", True, WHITE)
            self.score_txt = Texture.from_surface(renderer, self.score_surf)
            self.high_score_surf = font.render(f"BEST {self.high_score}", True, WHITE)
            self.high_score_txt = Texture.from_surface(renderer, self.high_score_surf)

            if self.time_since_last_hit < self.COMBO_TIME:
                self.current_combo += 1
                self.combo_surf = font.render(f"COMBO x{max(1,self.current_combo)}", True, WHITE)
                self.combo_txt = Texture.from_surface(renderer, self.combo_surf)
            if self.current_combo > 1:
                self.combo_counters.append(ComboCounter(hit.position, self.current_combo + 1))

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
                self.set_game_over()

            if bomb_status:
                self.bombs.remove(bomb)
                continue
            if (((not -bomb.radius * 2 < bomb.position.x < WIDTH + bomb.radius * 2) or
                 bomb.position.y - bomb.radius * 2 * bomb.RADIUS_FACTOR > HEIGHT) and bomb.velocity.y > 0):
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

    def set_game_over(self):
        self.game_over = True

        self.player.sliced_points.clear()
        pygame.mixer.Sound.play(self.bass_sound_effect)
        self.effects[4].append(FadeOutEffect(fade_time=self.GAME_OVER_TIME, max_alpha=20))

        if self.score > self.high_score:
            self.high_score = self.score
            with open(self.HIGH_SCORE_FILE, "w") as f:
                f.write(str(self.high_score))

        self.subtitle_surf = font.render(f"HIGH SCORE {self.high_score}", True, WHITE)

    def draw(self):
        self.BACKGROUND.draw(None, (0, 0))

        self.score_txt.draw(None, (7, 0))
        self.combo_txt.draw(None, (WIDTH / 2 - self.combo_txt.width / 2, 0))
        self.high_score_txt.draw(None, (WIDTH - self.high_score_txt.width - 7, 0))

        for effect in self.effects[0]:
            effect.draw()
        for effect in self.effects[1]:
            effect.draw()
        for bomb in self.bombs:
            bomb.draw()
        for effect in self.effects[2]:
            effect.draw()
        for fruit in self.fruits:
            fruit.draw()
        for effect in self.effects[3]:
            effect.draw()
        for combo in self.combo_counters:
            combo.draw()
        for effect in self.effects[4]:
            effect.draw()

        if self.game_over:
            self.r1.draw()
            self.r2.draw()
            self.game_over_txt.draw(None, (
                WIDTH / 2 - self.game_over_txt.width / 2, HEIGHT / 2 - self.game_over_txt.height / 2))
        self.player.draw()
