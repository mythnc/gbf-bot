import logging
from os.path import join
import random
import sys
import time
import pyautogui
from .constants import images_dir, battle_result_config as config
from . import utility
from .components import Button

logger = logging.getLogger(__name__)

result_ok = Button('ok1.png', config['result ok'])
to_next = Button('to_quest.png', config['to next'])
if config['has again'] == 'yes':
    to_next = Button('again.png', config['again'])
friend_cancel = Button('cancel.png', config['friend cancel'])


def activate():
    pyautogui.PAUSE = 1

    # wait before battle end
    logger.debug('wait before battle end')
    while True:
        time.sleep(0.5)
        found = utility.locate(result_ok.path, 0, 1/2, 1, 1/4)
        if found is not None:
            break

    logger.info('click result ok')
    result_ok.click()
    time.sleep(0.8 + random.random() * 0.25)

    chips_dialog()
    guild_wars_dialog()

    # wait before next step
    count = 0
    logger.debug('wait before next step')
    while True:
        # if characters' LB level up
        if count % 10 == 0:
            pyautogui.click()
        time.sleep(0.5)
        found = utility.locate(to_next.path, 0, 2/5, 1, 1/5)
        if found is not None:
            break
        count += 1

    logger.info('click to next')
    to_next.click()
    time.sleep(0.8)

    # friend request cancel if any
    found = utility.locate(friend_cancel.path, 0, 3/5, 1, 1/9)
    if found is not None:
        logger.info('click friend request cancel')
        friend_cancel.click()
        time.sleep(0.75 + random.random() * 0.35)

    halo_dialog()

def chips_dialog():
    # if De La Fille (Earth) in the party
    # there is chance casino chips dialog will be popped up
    if config['get chips'] == 'no':
        return

    chips_ok = Button('ok1.png', config['chips ok'])
    medal = join(images_dir, 'medal.png')
    found = utility.locate(medal, 0, 2/5, 1/2, 1/5)
    if found is not None:
        logger.info('chip dialog found')
        chips_ok.click()

def halo_dialog():
    # dimension halo if any
    # do not handle it, leave it to user
    if config['dimension halo'] == 'no':
        return

    dimension_close = Button('close.png', config['dimension close'])
    found = utility.locate(dimension_close.path, 0, 2/3, 1, 1/7)
    if found is not None:
        logger.info('dimension dialog found')
        logger.info('gbf robt finished')
        sys.exit(0)

def guild_wars_dialog():
    if config['guild wars'] == 'no':
        return

    count = 0
    ok = Button('ok1.png', config['guild wars ok'])
    while True:
        count += 1
        if count % 10 == 0:
            to_next.click()

        time.sleep(0.5)
        found = utility.locate(ok.path, 0, 2/3, 1, 1/6)
        if found is not None:
            logger.info('guild wars result dialog found')
            ok.click()
            return
