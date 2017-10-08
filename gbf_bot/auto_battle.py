import logging
from os.path import join
import time
import pyautogui
from . import buttons, package_root
from .components import Button

logger = logging.getLogger(__name__)

points = {}
with open(join(package_root, 'auto_battle_points')) as f:
    exec(f.read(), points)

attack = Button(buttons('attack.png'), points['attack'])
auto = Button(buttons('auto.png'), points['auto'])


def activate(battle_time):
    pyautogui.PAUSE = 1.5
    time.sleep(5)
    logger.info('click attack')
    attack.double_click()
    time.sleep(1)
    logger.info('click auto')
    auto.click()

    # battle result
    time.sleep(battle_time)
