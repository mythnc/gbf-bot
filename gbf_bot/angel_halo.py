import logging
from os.path import join
import time
import pyautogui
from . import angel_halo_config as points
from . import buttons, package_root, auto_battle, summon, battle_result
from .components import Button

logger = logging.getLogger(__name__)

angel_halo = Button(buttons('select.png'), points['angel_halo'])
angel_halo_level = Button(buttons('play.png'), points['angel_halo_level'])


def activate():
    pyautogui.PAUSE = 1.5
    # scroll mouse to the button
    logger.info('scroll mouse to the bottom')
    angel_halo.move_to()
    pyautogui.scroll(-20)

    # chose battle name
    # click twice for window choice
    logger.info('click angel halo')
    angel_halo.double_click()
    logger.info('click angel halo level')
    angel_halo_level.click()

    # AP will be checked before next step
    # make sure AP is enough

    # chose summon
    summon.activate()

    battle_time = 37
    auto_battle.activate(battle_time)

    battle_result.activate()
