import logging
from os.path import join
import random
import time
import pyautogui
from . import auto_battle_config as points
from . import buttons, package_root, battle_result_config
from .components import Button

logger = logging.getLogger(__name__)

attack = Button(buttons('attack.png'), points['attack'])
auto = Button(buttons('auto.png'), points['auto'])


def activate(battle_time):
    pyautogui.PAUSE = 1.3
    time.sleep(5)
    logger.info('click attack')
    attack.double_click()
    logger.info('click auto')
    auto.click()

    # battle result
    time.sleep(battle_time + random.random() * 3)
