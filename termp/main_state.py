import random
import json
import os

from pico2d import *

import game_framework
import start_state
from hero import Hero
from ground import Ground
from view import View

name = "MainState"

hero = None
ground = None
view = None
boss = None

def enter():
    global hero, ground, view
    hero = Hero()
    ground = Ground()
    view = View()

def exit():
    global hero, ground, view
    del(hero)
    del(ground)
    del(view)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(start_state)
            else:
                hero.handle_event(event)
def update(frame_time):
    hero.update(frame_time)
    if view.x < 3300:
        ground.update(frame_time)
        view.update(frame_time)

def draw_scene():
    view.draw()
    ground.draw()
    hero.draw()

def draw():
    clear_canvas()
    draw_scene()
    update_canvas()





