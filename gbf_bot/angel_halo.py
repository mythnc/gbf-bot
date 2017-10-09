import logging
from os.path import join
import random
import time
import pyautogui
from . import angel_halo_config as config
from . import buttons, package_root, auto_battle, summon, battle_result
from .components import Button

logger = logging.getLogger(__name__)

angel_halo = Button(buttons('select.png'), config['angel_halo'])
angel_halo_level = Button(buttons('play.png'), config['angel_halo_level'])


def activate():
    pyautogui.PAUSE = 1.5
    # scroll mouse to the button
    logger.info('scroll mouse to the bottom')
    angel_halo.move_to()
    pyautogui.scroll(-30)

    # chose battle name
    # click twice for window choice
    logger.info('click angel halo')
    angel_halo.double_click()
    time.sleep(random.random() * 0.25)
    logger.info('click angel halo level')
    angel_halo_level.click()
    time.sleep(random.random() * 0.25)

    # AP will be checked before next step
    # make sure AP is enough

    # chose summon
    summon.activate()

    battle_time = int(config['battle_time'])
    auto_battle.activate(battle_time)

    battle_result.activate()
