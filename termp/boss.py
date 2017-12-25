from pico2d import *

from ground import Ground

class BossFireball:
    image = None

    PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 20 cm
    RUN_SPEED_KMPH = 30.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4

    LEFT, RIGHT  = 0, 1

    def __init__(self):
        self.x, self.y = 0, 0
        self.frame = 0
        self.total_frames = 0.0
        self.dir = 1
        self.state = self.RIGHT
        if BossFireball.image == None:
            BossFireball.image = load_image('boss_fireball.png')

    def update(self, frame_time, isBoss):
        distance = BossFireball.RUN_SPEED_PPS * frame_time
        self.total_frames += BossFireball.FRAMES_PER_ACTION * BossFireball.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.x += self.dir*distance

    def draw(self):
        self.image.clip_draw(self.frame * 135, self.state * 45, 135, 45, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 60, self.y - 20, self.x + 60, self.y + 20

class Boss:
    image = None

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 5

    ALIVE, DEATH = 0, 1

    def __init__(self):
        self.x, self.y = 4600, 228
        self.frame = 0
        self.num = 0
        self.state = self.ALIVE
        self.hp = Boss_HP()
        self.hp.x, self.hp.y = self.x, self.y + 50
        self.total_frames = 0.0
        self.skill_count = 1
        if Boss.image == None:
            Boss.image = load_image('boss_alert.png')

    def update(self, frame_time, isBoss, boss_fireballs, hero):
        distance = Ground.RUN_SPEED_PPS * frame_time

        if isBoss:
            self.total_frames += Boss.FRAMES_PER_ACTION * Boss.ACTION_PER_TIME * frame_time
            self.frame = int(self.total_frames) % 5
        else:
            self.x -= distance

        self.hp.x, self.hp.y = self.x - (250 - self.hp.degree / 2), self.y + 200

        if self.hp.degree <= 0:
            self.state = self.DEATH

        if self.skill_count % 500 == 0 and isBoss:
            boss_fireball = BossFireball()
            boss_fireball.x = self.x
            boss_fireball.y = self.y - 30

            if hero.x - self.x > 0:
                boss_fireball.dir = 1
                boss_fireball.state = boss_fireball.RIGHT
            else:
                boss_fireball.dir = -1
                boss_fireball.state = boss_fireball.LEFT
            boss_fireballs.append(boss_fireball)
            self.skill_count = 1

        self.skill_count += 1

    def draw(self):
        self.image.clip_draw(self.frame * 250, 0, 250, 300, self.x, self.y)
        self.hp.draw()

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 150, self.x + 50, self.y + 150

class Boss_HP:
    image = None

    def __init__(self):
        self.x, self.y = 0, 0
        self.degree = 500
        if Boss_HP.image == None:
            Boss_HP.image = load_image('boss_hp.png')

    def draw(self):
        self.image.clip_draw(0, 0, self.degree, 20, self.x, self.y)