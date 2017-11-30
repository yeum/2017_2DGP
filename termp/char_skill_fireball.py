
from pico2d import *

from hero import Hero
from ground import Ground

class Fireball:
    PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 20 cm
    RUN_SPEED_KMPH = 15.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    def __init__(self):
        self.x, self.y = Hero.x, Hero.y
        self.frame = 0
        self.total_frames = 0.0
        self.dir = 0
        if Fireball.image == None:
            Fireball.image = load_image('fireball.png')

    def update(self, frame_time):
        distance = SDL_FillRect.RUN_SPEED_PPS * frame_time
        self.total_frames += Hero.FRAMES_PER_ACTION * Hero.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.x += (self.dir * distance)

    def draw(self):
        #self.image.draw(self.x, self.y)
        self.image.clip_draw(self.frame * 135, 0, 135, 45, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 65, self.y - 20, self.x + 65, self.y + 20


    def draw_bb(self):
        draw_rectangle(*self.get_bb())