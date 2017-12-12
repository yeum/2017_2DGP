from pico2d import *

from ground import Ground

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
        if Boss.image == None:
            Boss.image = load_image('boss_alert.png')

    def update(self, frame_time, isBoss):
        distance = Ground.RUN_SPEED_PPS * frame_time

        if isBoss:
            self.total_frames += Boss.FRAMES_PER_ACTION * Boss.ACTION_PER_TIME * frame_time
            self.frame = int(self.total_frames) % 5
        else:
            self.x -= distance

        self.hp.x, self.hp.y = self.x - (250 - self.hp.degree / 2), self.y + 200

        if self.hp.degree <= 0:
            self.state = self.DEATH

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