import logging
import random
import time
import pyautogui
from . import top_left, window_size
from . import auto_battle_config as config
from . import utility
from .components import Button

logger = logging.getLogger(__name__)


attack = Button('attack.png', config['attack'])
auto = Button('auto.png', config['auto'])


def activate(battle_time):
    pyautogui.PAUSE = 1.3

    # wait before battle start
    w, h = window_size
    start_pt = (top_left[0] + w//2, top_left[1] + h*1//3)
    region = start_pt + (w//2, h*2//3)
    while True:
        time.sleep(0.5)
        found = utility.locate(attack.path, region)
        if found is not None:
            break

    logger.info('click attack')
    attack.double_click()
    time.sleep(random.random() * 0.35)
    logger.info('click auto')
    auto.click()

    # battle result
    time.sleep(battle_time)
