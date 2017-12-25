import platform
import os

if platform.architecture()[0] == '32bit':
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x86"
else:
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x64"

import game_framework
from pico2d import*

import start_state
import main_state

open_canvas()
game_framework.run(start_state)
#테스트 할 모드를 넣어서 바로 테스트 할 수 있도록. 테스팅 시간을 절약한다.
close_canvas()