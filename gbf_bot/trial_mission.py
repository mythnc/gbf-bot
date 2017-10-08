import logging
from os.path import join
import time
import pyautogui
from . import buttons, package_root, auto_battle, summon, battle_result
from .components import Button

logger = logging.getLogger(__name__)

points = {}
with open(join(package_root, 'trial_points')) as f:
    exec(f.read(), points)

trial = Button(buttons('select.png'), points['trial'])
trial_level = Button(buttons('play.png'), points['trial_level'])


def activate():
    pyautogui.PAUSE = 1.5
    # chose battle name
    # click twice for window choice
    logger.info('click trial')
    trial.double_click()
    logger.info('click trial_level')
    trial_level.click()

    # AP will be checked before next step
    # make sure AP is enough

    # chose summon
    summon.activate()

    battle_time = 75
    auto_battle.activate(battle_time)

    battle_result.activate()
