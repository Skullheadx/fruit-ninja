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

        self.life_time = 0
        self.current_frame = 0

        self.surf_frames = random.choice(self.blood_frames)

        if color is None:
            color = random.choice(EFFECT_COLORS)

        for frame in self.surf_frames:
            px_array = pygame.PixelArray(frame)
            px_array.replace(pygame.Color(250, 3, 35), pygame.Color(color))
            px_array.close()

        self.frame_txt = [Texture.from_surface(renderer, frame) for frame in self.surf_frames]

    def update(self, delta):
        self.life_time += delta

        if self.life_time >= self.LIFE_TIME / len(self.surf_frames) * (self.current_frame + 1):
            self.current_frame += 1

        if self.life_time >= self.LIFE_TIME:
            return True

    def draw(self):
        if self.life_time < self.LIFE_TIME:
            self.frame_txt[self.current_frame].draw(None, pygame.Rect(self.position.x - self.radius,
                                                                      self.position.y - self.radius,
                                                                      self.radius * 2, self.radius * 2))


class BloodSplatter:
    LIFE_TIME = 4000
    FADE_TIME = 1000
    RADIUS_RANGE = [2, 2.75]
    ANGLE_OFFSET = 35
    blood_frames = [
        pygame.image.load("assets/effects/splatter/bloodslash1.png").convert_alpha(),
        pygame.image.load("assets/effects/splatter/bloodslash2.png").convert_alpha()
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
        self.angle = angle

        self.life_time = self.LIFE_TIME
        self.fade_time = self.FADE_TIME

        img_index = random.randint(0, len(self.blood_frames) - 1)
        self.alpha = 255

        if color is None:
            color = random.choice(EFFECT_COLORS)

        self.frame = Texture.from_surface(renderer, self.color_frames[img_index][color])

    def update(self, delta):
        if self.life_time > 0:
            self.life_time -= delta
        else:
            self.fade_time -= delta

        if self.fade_time <= 0 and self.life_time <= 0:
            return True

        if self.life_time <= 0:
            self.alpha = int(lerp(0, 255, self.fade_time / self.FADE_TIME))
            self.frame.alpha = self.alpha

    def draw(self):
        self.frame.draw(None, pygame.Rect(self.position.x - self.radius,
                                          self.position.y - self.radius,
                                          self.radius * 2, self.radius * 2),
                        self.angle + self.ANGLE_OFFSET, origin=(self.radius, self.radius))


class SplitEffect:
    SPEED_PERCENT_RANGE = [65, 85]
    gravity = 275

    def __init__(self, position, frame, fruit_velocity, normal_velocity):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(fruit_velocity) * lerp(self.SPEED_PERCENT_RANGE[0], self.SPEED_PERCENT_RANGE[1],
                                                              random.random()) / 100 + pygame.Vector2(normal_velocity)
        self.acceleration = pygame.Vector2(0, self.gravity)

        self.angle = 0
        self.direction = random.choice([-1, 1])

        self.frame = Texture.from_surface(renderer, frame)
        self.width, self.height = self.frame.width, self.frame.height

    def update(self, delta):
        self.velocity += self.acceleration * delta / 1000
        self.position += self.velocity * delta / 1000

        self.angle += 360 * delta / 1000 / 10 * self.direction

        if self.position.y - self.height / 2 > HEIGHT:
            return True

    def draw(self):
        self.frame.draw(None, pygame.Rect(self.position.x - self.width / 2,
                                          self.position.y - self.height / 2,
                                          self.width, self.height),
                        self.angle, origin=(self.width / 2, self.height / 2))
        self.width, self.height = self.frame.width, self.frame.height

    @staticmethod
    def find_normals(v):
        return pygame.Vector2(-v.y, v.x), pygame.Vector2(v.y, -v.x)

    @staticmethod
    def should_split(image, angle, image_position, mouse_position, mouse_direction, radius):
        img, img_pos = rotate_center(pygame.transform.scale(image.copy(), (radius * 2, radius * 2)), angle,
                                     image_position)
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
    def split_image(image, angle, image_position, mouse_position, mouse_direction, radius):
        img, img_pos = rotate_center(pygame.transform.scale(image.copy(), (radius * 2, radius * 2)), angle,
                                     image_position)


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

        p3 = (p1 - rot_center).rotate(-a) + rot_center

        half1 = img.subsurface(pygame.Rect(0, 0, img.get_width(), clamp(p3.y, 0, img.get_height())))
        half2 = img.subsurface(pygame.Rect(0, clamp(p3.y, 0, img.get_height()), img.get_width(),
                                           clamp(img.get_height() - p3.y, 0, img.get_height())))

        p5 = half1.get_rect().center - rot_center
        pos1 = p5.rotate(a) + img_pos

        p6 = half2.get_rect().center - rot_center + pygame.Vector2(0, clamp(p3.y, 0, img.get_height()))
        pos2 = p6.rotate(a) + img_pos

        r_half1 = pygame.transform.rotate(half1, -a)
        r_half2 = pygame.transform.rotate(half2, -a)

        return r_half1, r_half2, pos1, pos2


class SlashEffect:
    SLASH_SURFS = [pygame.image.load(f"assets/effects/sword_slashes/White_Slash_Thin/File{i}.png").convert_alpha()
                   for i in range(1, 7)]
    LIFETIME = 600

    def __init__(self, position, angle):
        self.position = pygame.Vector2(position)
        self.angle = angle

        self.time = 0
        self.current_frame = 0

        self.slash_frames = [Texture.from_surface(renderer, frame) for frame in self.SLASH_SURFS]

    def update(self, delta):
        self.time += delta
        if self.time >= self.LIFETIME / len(self.SLASH_SURFS):
            self.time = 0
            self.current_frame += 1
            if self.current_frame >= len(self.SLASH_SURFS):
                return True

    def draw(self):
        frame = self.slash_frames[self.current_frame]
        frame.draw(None, self.position - pygame.Vector2(frame.width, frame.height) / 2, self.angle)


class FadeInEffect:

    def __init__(self, fade_time=500):
        self.fade_time = fade_time
        self.surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.surf.fill(BLACK)
        self.time = self.fade_time
        self.alpha = 255

        self.txt = Texture.from_surface(renderer, self.surf)

    def update(self, delta):
        self.time -= delta

        if self.time <= 0:
            return True
        self.alpha = int(lerp(0, 255, self.time / self.fade_time))

    def draw(self):
        self.txt.alpha = self.alpha
        self.txt.draw(None, (0, 0))


class FadeOutEffect:

    def __init__(self, fade_time=500, max_alpha=255):
        self.fade_time = fade_time
        self.max_alpha = max_alpha

        self.surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.surf.fill(BLACK)
        self.time = 0
        self.alpha = 0

        self.txt = Texture.from_surface(renderer, self.surf)

    def update(self, delta):
        self.time += delta
        if self.time >= self.fade_time:
            return True
        self.alpha = int(lerp(0, self.max_alpha, self.time / self.fade_time))

    def draw(self):
        self.txt.alpha = self.alpha
        self.txt.draw(None, (0, 0))
