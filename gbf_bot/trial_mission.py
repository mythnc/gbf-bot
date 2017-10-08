import logging
from os.path import join
import time
import pyautogui
from . import buttons, package_root, auto_battle, summon, battle_result
from . import trial_mission_config as config
from .components import Button

logger = logging.getLogger(__name__)

trial = Button(buttons('select.png'), config['trial'])
trial_level = Button(buttons('play.png'), config['trial_level'])


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

    battle_time = int(config['battle_time'])
    auto_battle.activate(battle_time)

    battle_result.activate()
