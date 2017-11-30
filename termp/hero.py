import random

from pico2d import *

jump = None
top = None


class Hero:
    PIXEL_PER_METER = (10.0 / 0.2)           # 10 pixel 20 cm
    RUN_SPEED_KMPH = 10.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4

    image = None

    RIGHT_RUN, LEFT_RUN, RIGHT_DEATH, LEFT_DEATH, RIGHT_STAND, LEFT_STAND, RIGHT_ATTACK, LEFT_ATTACK, RIGHT_JUMP, LEFT_JUMP, RIGHT_SLIDE, LEFT_SLIDE = 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0

    def __init__(self):
        self.x, self.y = 50, 128 + 35
        self.frame = 0
        self.total_frames = 0.0
        self.dir = 0
        self.state = self.RIGHT_RUN
        self.y_for_collide = 35
        if Hero.image == None:
            Hero.image = load_image('character_sheet2.png')


    def update(self, frame_time, boss):
        global top, jump

        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        distance = Hero.RUN_SPEED_PPS * frame_time
        self.total_frames += Hero.FRAMES_PER_ACTION * Hero.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.x += (self.dir * distance)

        self.x = clamp(0, self.x, 800)

        if jump:
            self.is_top(boss)
            if top:
                self.y -= distance+0.3
            else:
                self.y += distance+0.3

    def get_height(self):
        return self.y


    def draw(self):
        self.image.clip_draw(self.frame * 70, self.state * 70, 70, 70, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - self.y_for_collide, self.x + 20, self.y + self.y_for_collide

    def handle_event(self, event, boss):
        global jump

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT) and boss:
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.RIGHT_RUN):
                self.state = self.LEFT_RUN
                self.dir = -1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT) and boss:
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.LEFT_RUN):
                self.state = self.RIGHT_RUN
                self.dir = 1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT) and boss:
            if self.state in (self.LEFT_RUN,):
                self.state = self.LEFT_STAND
                self.dir = 0
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT) and boss:
            if self.state in (self.RIGHT_RUN,):
                self.state = self.RIGHT_STAND
                self.dir = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            jump = True
            if self.state in (self.RIGHT_RUN, self.RIGHT_ATTACK, self.RIGHT_SLIDE, self.RIGHT_STAND):
                self.state = self.RIGHT_JUMP
            elif self.state in (self.LEFT_RUN, self.LEFT_ATTACK, self.LEFT_SLIDE, self.LEFT_STAND):
                self.state = self.LEFT_JUMP
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state in (self.RIGHT_RUN, self.RIGHT_STAND):
                self.state = self.RIGHT_SLIDE
                self.y_for_collide -= 30
                self.dir = 0
            elif self.state in (self.LEFT_RUN, self.LEFT_STAND):
                self.state = self.LEFT_SLIDE
                self.y_for_collide -= 30
                self.dir = 0
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.state in (self.RIGHT_SLIDE,):
                if boss:
                    self.state = self.RIGHT_STAND
                    self.y_for_collide += 30
                else:
                    self.state = self.RIGHT_RUN
                    self.y_for_collide += 30
            elif self.state in (self.LEFT_SLIDE,):
                if boss:
                    self.state = self.LEFT_STAND
                    self.y_for_collide += 30
                else:
                    self.state = self.LEFT_RUN
                    self.y_for_collide += 30
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            if self.state in (self.RIGHT_RUN, self.RIGHT_STAND):
                self.state = self.RIGHT_ATTACK
                self.dir = 0
            elif self.state in (self.LEFT_RUN, self.LEFT_STAND):
                self.state = self.LEFT_ATTACK
                self.dir = 0
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_SPACE):
            if self.state in (self.RIGHT_ATTACK,):
                if boss:
                    self.state = self.RIGHT_STAND
                else:
                    self.state = self.RIGHT_RUN
            elif self.state in (self.LEFT_ATTACK,):
                if boss:
                    self.state = self.LEFT_STAND
                else:
                    self.state = self.LEFT_RUN

    def is_top(self, boss):
        global jump, top
        if self.get_height() > 270:
            top = True
        elif self.get_height() < 128+35:
            self.y = 128+35
            jump = False
            top = False
            if self.state in (self.RIGHT_JUMP,):
                if boss:
                    self.state = self.RIGHT_STAND
                    self.dir = 0
                else:
                    self.state = self.RIGHT_RUN
            elif self.state in (self.LEFT_JUMP,):
                if boss:
                    self.state = self.LEFT_STAND
                    self.dir = 0
                else:
                    self.state = self.LEFT_RUN








