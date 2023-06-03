from bomb import Bomb
from combo_counter import ComboCounter
from effect import Effect
from fruit import Fruit
from player import Player
from setup import *


class Game:
    BOMB_CHANCE = 0.1
    EFFECT_COUNT_PER_FRUIT = 20
    EFFECT_COUNT_PER_BOMB = 0
    COMBO_TIME = 250
    GAME_OVER_TIME = 2000

    def __init__(self):
        self.player = Player()
        self.fruits = [Fruit()]
        self.bombs = []
        self.effects = []
        self.combo_counters = []
        self.wave = 1
        self.score = 0
        self.time_since_last_hit = 0
        self.current_combo = 0

        self.game_over = False
        self.game_over_time = 0

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return COMMAND_EXIT
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return COMMAND_EXIT

        if not self.game_over:
            self.player.update(delta)
        else:
            self.game_over_time += delta
            if self.game_over_time > self.GAME_OVER_TIME:
                return COMMAND_START
        hits = []
        for fruit in self.fruits:
            fruit.update(delta)
            if self.player.hits(fruit):
                hits.append(fruit)
            fr = fruit.get_rect()
            if ((not -fruit.radius < fr.x < WIDTH + fruit.radius) or fr.y > HEIGHT) and fruit.velocity.y > 0:
                self.fruits.remove(fruit)
        self.time_since_last_hit += delta

        if self.time_since_last_hit < self.COMBO_TIME:
            self.score += self.current_combo
        else:
            self.current_combo = 0
        for hit in hits:
            for i in range(self.EFFECT_COUNT_PER_FRUIT):
                self.effects.append(Effect(hit.position, hit.radius, hit.color))
            if hit in self.fruits:
                self.fruits.remove(hit)
            self.score += 1
            if self.time_since_last_hit < self.COMBO_TIME:
                self.current_combo += 1
                if self.current_combo > 1:
                    self.combo_counters.append(ComboCounter(hit.position, f"x{self.current_combo + 1}"))

            self.time_since_last_hit = 0

        for effect in self.effects:
            effect_status = effect.update(delta)
            if effect_status:
                self.effects.remove(effect)

        for combo in self.combo_counters:
            combo_status = combo.update(delta)
            if combo_status:
                self.combo_counters.remove(combo)

        for bomb in self.bombs:
            bomb.update(delta)
            if self.player.hits(bomb):
                for i in range(self.EFFECT_COUNT_PER_BOMB):
                    self.effects.append(
                        Effect(bomb.position + pygame.Vector2(random.random(), random.random()), bomb.radius, WHITE,
                               darken=False))

                bomb.explode(self.fruits, self.bombs, self.effects)
                self.game_over = True
                self.player.sliced_points.clear()
            br = bomb.get_rect()
            if ((not -bomb.RADIUS < br.x < WIDTH + bomb.RADIUS) or br.y > HEIGHT) and bomb.velocity.y > 0:
                self.bombs.remove(bomb)

        if len(self.fruits) == 0 and len(self.bombs) == 0:
            self.wave += 1
            for i in range(self.wave):
                if random.random() < self.BOMB_CHANCE:
                    self.bombs.append(Bomb())
                else:
                    self.fruits.append(Fruit())

    def draw(self, surf):
        screen.fill(BROWN)
        for effect in self.effects:
            effect.draw(surf)
        for bomb in self.bombs:
            bomb.draw(surf)
        for fruit in self.fruits:
            fruit.draw(surf)
        for combo in self.combo_counters:
            combo.draw(surf)
        self.player.draw(surf)
        text_surf = font.render(f"SCORE {self.score}", True, WHITE)
        surf.blit(text_surf, (0, 0))
        # text_surf2 = font.render(f"COMBO {self.current_combo}", True, WHITE)
        # surf.blit(text_surf2, (0, text_surf.get_height()))
        # text_surf2 = font.render(f"TIME SINCE LAST HIT {round(self.time_since_last_hit / 1000, 1)}", True, BLACK)
        # surf.blit(text_surf2, (WIDTH - text_surf2.get_width(), text_surf.get_height()))

        if self.game_over:
            game_over_surf = font_large.render("GAME OVER", True, WHITE)
            surf.blit(game_over_surf, game_over_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2.5)))
