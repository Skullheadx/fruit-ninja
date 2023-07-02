import pygame

from setup import *


class BloodEffect:
    LIFE_TIME = 1000
    SPEED_RANGE = [250, 350]
    RADIUS_RANGE = [3, 3.75]
    blood_frames = [
        [pygame.image.load(f"assets/effects/blood1/{i}.png").convert_alpha() for i in range(16)],
        [pygame.image.load(f"assets/effects/blood2/{i}.png").convert_alpha() for i in range(16)],
        [pygame.image.load(f"assets/effects/blood3/{i}.png").convert_alpha() for i in range(16)]
    ]

    def __init__(self, position, radius, color=None):
        self.position = pygame.Vector2(position)
        self.radius = radius * lerp(self.RADIUS_RANGE[0], self.RADIUS_RANGE[1], random.random())
        self.time = self.LIFE_TIME
        self.frame_timer = 0
        self.current_frame = 0
        self.angle = 0
        self.frames = [
            pygame.transform.rotate(pygame.transform.scale(frame, (int(self.radius * 2), int(self.radius * 2))),
                                    self.angle) for frame in random.choice(self.blood_frames)]
        if color is None:
            color = random.choice(EFFECT_COLORS)
        else:
            color = color
        for frame in self.frames:
            px_array = pygame.PixelArray(frame)
            px_array.replace(pygame.Color(250, 3, 35), pygame.Color(color))
            px_array.close()

    def update(self, delta):
        self.time -= delta
        self.frame_timer += delta
        if self.frame_timer >= self.LIFE_TIME / len(self.frames):
            self.frame_timer = 0
            self.current_frame += 1
        if self.time <= 0:
            return True

    def draw(self, surf):
        if self.time > 0:
            surf.blit(self.frames[self.current_frame], (self.position.x - self.radius, self.position.y - self.radius))
            # pygame.draw.circle(surf, BLACK, self.position, self.radius)


class BloodSplatter:
    LIFE_TIME = 4000
    FADE_TIME = 1000
    RADIUS_RANGE = [3, 3.75]
    blood_frames = [
        pygame.transform.rotate(pygame.image.load(
            "assets/effects/splatter/bloodslash1.png"),
            -35).convert_alpha(),
        pygame.transform.rotate(pygame.image.load(
            "assets/effects/splatter/bloodslash2.png"),
            -35).convert_alpha()
    ]

    LIGHT_COLOR1 = pygame.Color(110, 110, 110)
    DARK_COLOR1 = pygame.Color(84, 84, 84)
    LIGHT_COLOR2 = pygame.Color(83, 83, 83)
    DARK_COLOR2 = pygame.Color(74, 74, 74)


    color_frames = [dict(), dict()]
    for c in EFFECT_COLORS:
        for i, f in enumerate(blood_frames):
            c_f = f.copy()
            px_array = pygame.PixelArray(c_f)
            px_array.replace(LIGHT_COLOR1 if i == 0 else LIGHT_COLOR2, pygame.Color(c))
            px_array.replace(DARK_COLOR1 if i == 0 else DARK_COLOR2, pygame.Color(darken(c, 0.875)))
            px_array.close()
            color_frames[i][c] = c_f


    def __init__(self, position, radius, angle, color=None):
        self.position = pygame.Vector2(position)
        self.radius = radius * lerp(self.RADIUS_RANGE[0], self.RADIUS_RANGE[1], random.random())
        self.time = self.LIFE_TIME
        self.fade_time = self.FADE_TIME
        self.angle = angle
        img_index = random.randint(0, len(self.blood_frames) - 1)
        # self.frame = pygame.transform.rotate(
        #     pygame.transform.scale(self.blood_frames[img_index], (int(self.radius * 2), int(self.radius * 2))),
        #     self.angle)
        self.alpha = 255

        if color is None:
            color = random.choice(EFFECT_COLORS)

        self.frame = pygame.transform.rotate(
            pygame.transform.scale(self.color_frames[img_index][color], (int(self.radius * 2), int(self.radius * 2))),
            self.angle)

        # px_array = pygame.PixelArray(self.frame)
        # px_array.replace(self.LIGHT_COLOR1 if img_index == 0 else self.LIGHT_COLOR2, pygame.Color(color))
        # px_array.replace(self.DARK_COLOR1 if img_index == 0 else self.DARK_COLOR2, pygame.Color(darken(color, 0.875)))
        # px_array.close()

    def update(self, delta):
        if self.time > 0:
            self.time -= delta
        else:
            self.fade_time -= delta

        if self.fade_time <= 0 and self.time <= 0:
            return True
        if self.time <= 0:
            self.alpha = int(lerp(0, 255, self.fade_time / self.FADE_TIME))

    def draw(self, surf):

        self.frame.set_alpha(self.alpha)
        surf.blit(self.frame, (self.position.x - self.radius, self.position.y - self.radius))


class SplitEffect:
    SPEED_PERCENT_RANGE = [65, 85]
    gravity = 275

    def __init__(self, position, frame, fruit_velocity, normal_velocity):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(fruit_velocity) * lerp(self.SPEED_PERCENT_RANGE[0], self.SPEED_PERCENT_RANGE[1],
                                                              random.random()) / 100 + pygame.Vector2(normal_velocity)
        self.acceleration = pygame.Vector2(0, self.gravity)

        # self.angle = lerp(-45, 45, random.random())
        self.angle = 0
        self.direction = random.choice([-1, 1])
        # self.angle = 0
        # self.direction = 0

        self.frame = frame

        self.width, self.height = self.frame.get_size()

    def update(self, delta):
        self.velocity += self.acceleration * delta / 1000
        self.position += self.velocity * delta / 1000
        self.angle += 360 * delta / 1000 / 10 * self.direction

        if self.position.y - self.height / 2 > HEIGHT:
            return True

    def draw(self, surf):
        rotated_image, position = rotate_center(self.frame, self.angle, self.position)
        self.width, self.height = rotated_image.get_size()
        surf.blit(rotated_image, position)

    @staticmethod
    def find_normals(v):
        return pygame.Vector2(-v.y, v.x), pygame.Vector2(v.y, -v.x)

    @staticmethod
    def should_split(image, angle, image_position, mouse_position, mouse_direction):
        img, img_pos = rotate_center(image.copy(), angle, image_position)
        img_pos += pygame.Vector2(img.get_size()) / 2
        if mouse_direction.x == 0:
            mouse_direction.x += 0.0001
        a = math.degrees(math.atan(mouse_direction.y / mouse_direction.x))
        img = rotate_center(img, a, pygame.Vector2(0, 0))[0]

        top_left = pygame.Vector2(image_position) - pygame.Vector2(img.get_width() / 2, img.get_height() / 2)
        rot_center = pygame.Vector2(image_position) - top_left
        mp = mouse_position - top_left

        t1 = (- mp.x) / mouse_direction.x
        p1 = mp + t1 * mouse_direction

        p3 = (p1 - rot_center).rotate(-a) + rot_center

        MIN_SPLIT = 0.25
        slice_percent = clamp(p3.y, 0, img.get_height()) / img.get_height()
        if MIN_SPLIT < slice_percent < 1 - MIN_SPLIT:
            return True
        return False

    @staticmethod
    def split_image(image, angle, image_position, mouse_position, mouse_direction):
        img, img_pos = rotate_center(image.copy(), angle, image_position)
        img_pos += pygame.Vector2(img.get_size()) / 2
        if mouse_direction.x == 0:
            mouse_direction.x += 0.0001

        a = math.degrees(math.atan(mouse_direction.y / mouse_direction.x))
        img = rotate_center(img, a, pygame.Vector2(0, 0))[0]

        top_left = pygame.Vector2(img_pos) - pygame.Vector2(img.get_width() / 2, img.get_height() / 2)
        rot_center = pygame.Vector2(img_pos) - top_left

        # finding end and start points of the splitting line
        # [x,y] = mouse_position + t * mouse_direction # vector equation
        # x = mouse_position.x + t * mouse_direction.x
        # y = mouse_position.y + t * mouse_direction.y

        mp = mouse_position - top_left

        t1 = (- mp.x) / mouse_direction.x
        p1 = mp + t1 * mouse_direction

        t2 = (img.get_width() - mp.x) / mouse_direction.x
        p2 = mp + t2 * mouse_direction

        p3 = (p1 - rot_center).rotate(-a) + rot_center
        p4 = (p2 - rot_center).rotate(-a) + rot_center

        half1 = img.subsurface(pygame.Rect(0, 0, img.get_width(), clamp(p3.y, 0, img.get_height())))
        half2 = img.subsurface(pygame.Rect(0, clamp(p3.y, 0, img.get_height()), img.get_width(),
                                           clamp(img.get_height() - p3.y, 0, img.get_height())))

        p5 = half1.get_rect().center - rot_center
        pos1 = (p5).rotate(a) + img_pos

        p6 = half2.get_rect().center - rot_center + pygame.Vector2(0, clamp(p3.y, 0, img.get_height()))
        pos2 = (p6).rotate(a) + img_pos

        r_half1 = pygame.transform.rotate(half1, -a)
        r_half2 = pygame.transform.rotate(half2, -a)

        return r_half1, r_half2, pos1, pos2


class SlashEffect:
    SLASH = [pygame.image.load(f"assets/effects/sword_slashes/White_Slash_Thin/File{i}.png").convert_alpha() for i in
             range(1, 7)]
    GROUP_SLASH = [pygame.image.load(f"assets/effects/sword_slashes/White_Group_Slashes/File{i}.png").convert_alpha()
                   for i in
                   range(1, 21)]
    LIFETIME = 600

    def __init__(self, position, angle, combo=False):
        self.position = pygame.Vector2(position)
        self.angle = angle

        self.is_combo = combo

        self.time = 0
        self.frame = 0

        # if self.is_combo:
        #     self.slash_frames = [pygame.transform.rotate(frame, self.angle) for frame in self.GROUP_SLASH]
        # else:
        #     self.slash_frames = [pygame.transform.rotate(frame, self.angle) for frame in self.SLASH]
        if self.is_combo:
            self.slash_frames = self.GROUP_SLASH
        else:
            self.slash_frames = [pygame.transform.rotate(frame, self.angle) for frame in self.SLASH]

    def update(self, delta):
        self.time += delta
        if self.time >= self.LIFETIME / len(self.SLASH):
            self.time = 0
            self.frame += 1
            if self.frame >= len(self.SLASH):
                return True

    def draw(self, surf):

        frame = self.slash_frames[self.frame]
        surf.blit(frame, frame.get_rect(center=self.position))


class FadeInEffect:

    def __init__(self, fade_time=500):
        self.fade_time = fade_time
        self.surf = pygame.Surface((WIDTH, HEIGHT))
        self.surf.fill(BLACK)
        self.time = self.fade_time
        self.alpha = 255

    def update(self, delta):
        self.time -= delta

        if self.time <= 0:
            return True
        self.alpha = int(lerp(0, 255, self.time / self.fade_time))

    def draw(self, surf):
        self.surf.set_alpha(self.alpha)
        surf.blit(self.surf, (0, 0))


class FadeOutEffect:

    def __init__(self, fade_time=500, max_alpha=255):
        self.fade_time = fade_time
        self.max_alpha = max_alpha

        self.surf = pygame.Surface((WIDTH, HEIGHT))
        self.surf.fill(BLACK)
        self.time = 0
        self.alpha = 0

    def update(self, delta):
        self.time += delta
        if self.time >= self.fade_time:
            return True
        self.alpha = int(lerp(0, self.max_alpha, self.time / self.fade_time))

    def draw(self, surf):
        self.surf.set_alpha(self.alpha)
        surf.blit(self.surf, (0, 0))
