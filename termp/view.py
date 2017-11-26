
from pico2d import *

class View:
    PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 20 cm
    RUN_SPEED_KMPH = 10.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self):
        self.image = load_image('map_view.png')
        self.x, self.y = 1750, 300 + 64

    def update(self, frame_time):
        distance = View.RUN_SPEED_PPS * frame_time
        self.x -= distance

    def draw(self):
        self.image.draw(self.x, self.y)
        #self.image.clip_draw(0, 0, 800, 600, self.x, self.y)