import logging
import random
import time
import pyautogui
from .constants import auto_battle_config as config
from . import utility
from .components import Button

logger = logging.getLogger(__name__)


attack = Button('attack.png', config['attack'])
auto = Button('auto.png', config['auto'])


def activate(battle_time):
    pyautogui.PAUSE = 1.3

    # wait before battle start
    while True:
        time.sleep(0.5)
        found = utility.locate(attack.path, 1/2, 1/3, 1/2, 2/3)
        if found is not None:
            break

    pyautogui.PAUSE = 1.3
    logger.info('click attack')
    attack.double_click()
    time.sleep(1 + random.random() * 0.35)
    logger.info('click auto')
    auto.click(partition=12)

    # battle result
    time.sleep(battle_time)
