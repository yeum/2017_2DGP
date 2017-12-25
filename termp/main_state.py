import random
import json
import os

from pico2d import *

import game_framework
import start_state
from hero import Hero, Char_Effect
from ground import Ground
from view import View
from boss import Boss

name = "MainState"

hero = None
ground = None
view = None
isBoss = None
isClear = None
collide_box_on = None

fireballs = []
boss_fireballs = []
effects = []

class Stone:
    image = None


    ALIVE, DEATH = 0, 1

    def __init__(self):
        self.x, self.y = 0, 153
        self.state = self.ALIVE
        self.num = 0
        if Stone.image == None:
            Stone.image = load_image('obs_stone.png')

    def update(self, frame_time, isBoss):
        distance = Ground.RUN_SPEED_PPS * frame_time
        if isBoss == None:
            self.x -= distance

    def draw(self):
        self.image.draw(self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 20, self.x + 20, self.y + 20

class Boom:
    image = None


    ALIVE, DEATH = 0, 1

    def __init__(self):
        self.x, self.y = 0, 220
        self.state = self.ALIVE
        self.num = 0
        if Boom.image == None:
            Boom.image = load_image('obs_boom.png')

    def update(self, frame_time, isBoss):
        distance = Ground.RUN_SPEED_PPS * frame_time
        if isBoss == None:
            self.x -= distance

    def draw(self):
        self.image.draw(self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 40, self.y - 45, self.x + 40, self.y + 45

class Drink:
    image = None


    ALIVE, DEATH = 0, 1

    def __init__(self):
        self.x, self.y = 0, 158
        self.state = self.ALIVE
        self.num = 0
        if Drink.image == None:
            Drink.image = load_image('obs_drink.png')

    def update(self, frame_time, isBoss):
        distance = Ground.RUN_SPEED_PPS * frame_time
        if isBoss == None:
            self.x -= distance

    def draw(self):
        self.image.draw(self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 12, self.y - 30, self.x + 12, self.y + 30

class Monster:
    image = None

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    ALIVE, DEATH = 0, 1

    def __init__(self):
        self.x, self.y = 0, 158
        self.frame = 0
        self.num = 0
        self.state = self.ALIVE
        self.total_frames = 0.0
        if Monster.image == None:
            Monster.image = load_image('obs_monster.png')

    def update(self, frame_time, isBoss):
        distance = Ground.RUN_SPEED_PPS * frame_time
        self.total_frames += Monster.FRAMES_PER_ACTION * Monster.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 6
        if isBoss == None:
            self.x -= distance

    def draw(self):
        self.image.clip_draw(self.frame * 80, 0, 80, 60, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25, self.y - 15, self.x + 10, self.y + 15

class Clear:
    image = None

    def __init__(self):
        self.x, self.y = 400, 400
        if Clear.image == None:
            Clear.image = load_image('clear.png')

    def draw(self):
        self.image.draw(self.x, self.y)

class Fail:
    image = None

    def __init__(self):
        self.x, self.y = 400, 400
        if Fail.image == None:
            Fail.image = load_image('fail.png')

    def draw(self):
        self.image.draw(self.x, self.y)


def enter():
    global hero, ground, view, stones, mons, drinks, booms, boss, isBoss, isClear, clear, fail
    clear = Clear()
    fail = Fail()
    isBoss = None
    isClear = None
    stones = create_stones()
    mons = create_mons()
    drinks = create_drinks()
    booms = create_booms()
    boss = Boss()
    hero = Hero()
    ground = Ground()
    view = View()


def exit():
    global hero, ground, view, mons, stones, booms, drinks, fireballs, boss, effects, boss_fireballs, clear, fail
    del(hero)
    del(ground)
    del(view)
    del(boss)
    del(clear)
    del(fail)
    for obj_mon in mons:
        del(obj_mon)
    for obj_stone in stones:
        del(obj_stone)
    for obj_boom in booms:
        del(obj_boom)
    for obj_drink in drinks:
        del(obj_drink)
    for skill_fireball in fireballs:
        del(skill_fireball)
    for skill_effect in effects:
        del(skill_effect)
    for boss_fireball in boss_fireballs:
        del(boss_fireball)

def handle_events(frame_time):
    global isBoss, collide_box_on, fireballs
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(start_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
                if collide_box_on:
                    collide_box_on = False
                else:
                    collide_box_on = True
            else:
                hero.handle_event(event, isBoss, fireballs)

def update(frame_time):
    global isBoss, isClear

    if view.x <= -950:
        isBoss = True

    hero.update(frame_time, isBoss)


    if hero.state not in (hero.RIGHT_DEATH, hero.LEFT_DEATH):
        ground.update(frame_time, isBoss)
        view.update(frame_time, isBoss)

        if isClear == None:
            boss.update(frame_time, isBoss, boss_fireballs, hero)

        for obj_stone in stones:
            if collide(hero, obj_stone):
                stones.remove(obj_stone)
                hero.crush()
                hero.tired.degree += 20
            else:
                obj_stone.update(frame_time, isBoss)

        for obj_mon in mons:
            if collide(hero, obj_mon):
                mons.remove(obj_mon)
                hero.crush()
                hero.tired.degree += 20
            else:
                obj_mon.update(frame_time, isBoss)

        for obj_boom in booms:
            if collide(hero, obj_boom):
                booms.remove(obj_boom)
                hero.crush()
                hero.tired.degree += 20
            else:
                obj_boom.update(frame_time, isBoss)

        for obj_drink in drinks:
            if collide(hero, obj_drink):
                drinks.remove(obj_drink)
                hero.eat()
                hero.tired.degree -= 30
                if hero.tired.degree < 0:
                    hero.tired.degree = 0
            else:
                obj_drink.update(frame_time, isBoss)

        for skill_fireball in fireballs:
            skill_fireball.update(frame_time, isBoss)

        for boss_fireball in boss_fireballs:
            boss_fireball.update(frame_time, isBoss)

        for skill_fireball in fireballs:
            for obj_stone in stones:
                if collide(skill_fireball, obj_stone):
                    fireballs.remove(skill_fireball)
                    hero.hit()
                    skill_effect = Char_Effect()
                    skill_effect.x = obj_stone.x
                    skill_effect.y = obj_stone.y
                    effects.append(skill_effect)
            for obj_mon in mons:
                if collide(skill_fireball, obj_mon):
                    mons.remove(obj_mon)
                    fireballs.remove(skill_fireball)
                    hero.hit()
                    skill_effect = Char_Effect()
                    skill_effect.x = obj_mon.x
                    skill_effect.y = obj_mon.y
                    effects.append(skill_effect)
            for obj_boom in booms:
                if collide(skill_fireball, obj_boom):
                    fireballs.remove(skill_fireball)
                    hero.hit()
                    skill_effect = Char_Effect()
                    skill_effect.x = obj_boom.x
                    skill_effect.y = obj_boom.y
                    effects.append(skill_effect)
            if isBoss:
                if collide(skill_fireball, boss):
                    fireballs.remove(skill_fireball)
                    hero.hit()
                    skill_effect = Char_Effect()
                    skill_effect.x = boss.x
                    skill_effect.y = boss.y
                    effects.append(skill_effect)
                    boss.hp.degree -= 50

        for boss_fireball in boss_fireballs:
            if collide(boss_fireball, hero):
                boss_fireballs.remove(boss_fireball)
                hero.crush()
                hero.tired.degree += 20

        if boss.state == boss.DEATH:
            isClear = True

    for skill_effect in effects:
        skill_effect.update(frame_time, isBoss)

        if skill_effect.frame >= 5:
            effects.remove(skill_effect)

def draw_scene(frame_time):
    global isClear

    view.draw()
    ground.draw()
    hero.draw()
    if isClear == None:
        boss.draw()
    for obj_stone in stones:
        obj_stone.draw()
    for obj_mon in mons:
        obj_mon.draw()
    for obj_boom in booms:
        obj_boom.draw()
    for obj_drink in drinks:
        obj_drink.draw()
    for skill_fireball in fireballs:
        skill_fireball.draw()
    for skill_effect in effects:
        skill_effect.draw()
    for boss_fireball in boss_fireballs:
        boss_fireball.draw()

    if collide_box_on:
        hero.draw_bb()
        boss.draw_bb()
        for obj_stone in stones:
            obj_stone.draw_bb()
        for obj_mon in mons:
            obj_mon.draw_bb()
        for obj_boom in booms:
            obj_boom.draw_bb()
        for obj_drink in drinks:
            obj_drink.draw_bb()
        for fireball in fireballs:
            fireball.draw_bb()
        for boss_fireball in boss_fireballs:
            boss_fireball.draw_bb()

    if hero.state in (hero.RIGHT_DEATH, hero.LEFT_DEATH):
        fail.draw()
    if isClear:
        clear.draw()

def draw(frame_time):
    clear_canvas()
    draw_scene(frame_time)
    update_canvas()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def create_stones():
    stones_data_file = open('obs_stone.txt', 'r')
    stones_data = json.load(stones_data_file)
    stones_data_file.close()

    stones = []

    for num in stones_data:
        obj_stone = Stone()
        obj_stone.num = num
        obj_stone.x = stones_data[num]['x']
        obj_stone.state = stones_data[num]['StartState']
        stones.append(obj_stone)

    return stones

def create_mons():
    mons_data_file = open('obs_monster.txt', 'r')
    mons_data = json.load(mons_data_file)
    mons_data_file.close()

    mons = []

    for num in mons_data:
        obj_mon = Monster()
        obj_mon.num = num
        obj_mon.x = mons_data[num]['x']
        obj_mon.state = mons_data[num]['StartState']
        mons.append(obj_mon)

    return mons

def create_booms():
    booms_data_file = open('obs_boom.txt', 'r')
    booms_data = json.load(booms_data_file)
    booms_data_file.close()

    booms = []

    for num in booms_data:
        obj_boom = Boom()
        obj_boom.num = num
        obj_boom.x = booms_data[num]['x']
        obj_boom.state = booms_data[num]['StartState']
        booms.append(obj_boom)

    return booms

def create_drinks():
    drinks_data_file = open('obs_drink.txt', 'r')
    drinks_data = json.load(drinks_data_file)
    drinks_data_file.close()

    drinks = []

    for num in drinks_data:
        obj_drink = Drink()
        obj_drink.num = num
        obj_drink.x = drinks_data[num]['x']
        obj_drink.state = drinks_data[num]['StartState']
        drinks.append(obj_drink)

    return drinks


