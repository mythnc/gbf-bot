import logging
from os.path import join
import time
import pyautogui
from . import images_dir, package_root
from .components import Button

logger = logging.getLogger(__name__)

points = {}
with open(join(package_root, 'trial_points')) as f:
    exec(f.read(), points)

buttons_dir = lambda x: join(images_dir, 'buttons', x)
trial = Button(buttons_dir('select.png'), points['trial'])
trial_level = Button(buttons_dir('play.png'), points['trial_level'])
summon = Button(buttons_dir('summon.png'), points['summon'])
summon_ok = Button(buttons_dir('ok2.png'), points['summon_ok'])
attack = Button(buttons_dir('attack.png'), points['attack'])
auto = Button(buttons_dir('auto.png'), points['auto'])
result_ok = Button(buttons_dir('ok1.png'), points['result_ok'])
to_quest = Button(buttons_dir('to_quest.png'), points['to_quest'])
friend_cancel = Button(buttons_dir('cancel.png'), points['friend_cancel'],
                       False)
explanation_ok = Button(buttons_dir('ok1.png'), points['explanation_ok'])


def activate():
    # chose battle name
    # click twice for window choice
    logger.info('click trial')
    trial.double_click()
    logger.info('click trial_level')
    trial_level.click()

    # AP will be checked before next step
    # make sure AP is enough

    # chose summon
    time.sleep(1)
    logger.info('click summon')
    summon.click()
    logger.info('click ok')
    summon_ok.click()

    # battle start
    time.sleep(5)
    logger.info('click attack')
    attack.click()
    time.sleep(1)
    logger.info('click auto')
    auto.click()

    # battle result
    time.sleep(75)
    logger.info('click result ok')
    result_ok.double_click()
    time.sleep(2)
    logger.info('click to quest')
    to_quest.double_click(0)
    # friend request cancel
    logger.info('click friend request cancel')
    friend_cancel.click()

    # foolproof
    logger.info('click ok')
    explanation_ok.click(0)
