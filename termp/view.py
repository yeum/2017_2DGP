import random

from pico2d import *

class View:
    def __init__(self):
        self.image = load_image('view.png')

    def draw(self):
        self.image.draw(400, 271)