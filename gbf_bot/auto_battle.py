import logging
import random
import time
import pyautogui
from . import auto_battle_config as config
from .components import Button

logger = logging.getLogger(__name__)

attack = Button('attack.png', config['attack'])
auto = Button('auto.png', config['auto'])


def activate(battle_time):
    pyautogui.PAUSE = 1.3
    time.sleep(5 + random.random() * 0.25)
    logger.info('click attack')
    attack.double_click()
    time.sleep(random.random() * 0.35)
    logger.info('click auto')
    auto.click()

    # battle result
    time.sleep(battle_time + random.random() * 3)
