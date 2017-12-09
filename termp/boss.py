from pico2d import *

from ground import Ground

class Boss:
    image = None

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 5

    ALIVE, DEATH = 0, 1

    def __init__(self):
        self.x, self.y = 4600, 278
        self.frame = 0
        self.num = 0
        self.state = self.ALIVE
        self.total_frames = 0.0
        if Boss.image == None:
            Boss.image = load_image('boss_alert.png')

    def update(self, frame_time, isBoss):
        distance = Ground.RUN_SPEED_PPS * frame_time
        self.total_frames += Boss.FRAMES_PER_ACTION * Boss.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 5
        if isBoss == None:
            self.x -= distance

    def draw(self):
        self.image.clip_draw(0, 0, 250, 300, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25, self.y - 15, self.x + 10, self.y + 15