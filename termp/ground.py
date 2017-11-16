import random

from pico2d import *

class Ground:
    def __init__(self):
        self.image = load_image('ground.png')

    def draw(self):
        self.image.draw(400, 64)

    def get_bb(self):
        return 0, 0, 800, 128

    def draw_bb(self):
        draw_rectangle(*self.get_bb())