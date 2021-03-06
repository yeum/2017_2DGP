# 시작화면, 난이도 선택

import game_framework
import help_state
from pico2d import *

from hero import Hero

name = "StartState"
image = None

hero = None

def create_world():
    global hero
    hero = Hero()

def destroy_world():
    global hero
    del(hero)

def enter():
    global image
    game_framework.reset_time()
    image = load_image('start.png')
    create_world()


def exit():
    global image
    del(image)
    destroy_world()


def draw(frame_time):
    global image
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(help_state)



def update(frame_time):
    pass

def pause(): pass


def resume(): pass




