import game_framework
from pico2d import*

import start_state
import main_state

open_canvas()
game_framework.run(start_state)
#테스트 할 모드를 넣어서 바로 테스트 할 수 있도록. 테스팅 시간을 절약한다.
close_canvas()