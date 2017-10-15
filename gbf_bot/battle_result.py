import logging
from os.path import join
import random
import sys
import time
import pyautogui
from . import top_left, window_size, images_dir
from . import battle_result_config as config
from . import utility
from .components import Button

logger = logging.getLogger(__name__)

result_ok = Button('ok1.png', config['result ok'])
to_quest = Button('to_quest.png', config['to quest'])
friend_cancel = Button('cancel.png', config['friend cancel'])


def activate():
    pyautogui.PAUSE = 1

    # wait before battle end
    w, h = window_size
    x, y = top_left
    region = (x, y+h//2) + (w, h//4)
    logger.debug('wait before battle end')
    while True:
        time.sleep(0.5)
        found = utility.locate(result_ok.path, region)
        if found is not None:
            break

    logger.info('click result ok')
    result_ok.double_click()
    time.sleep(0.8 + random.random() * 0.25)

    chips_dialog()

    # wait before next step
    region = (x, y+h//2) + (w, h//15)
    count = 0
    logger.debug('wait before next step')
    while True:
        # if characters' LB level up
        if count % 10 == 0:
            pyautogui.click()
        time.sleep(0.5)
        found = utility.locate(to_quest.path, region)
        if found is not None:
            break
        count += 1

    logger.info('click to quest')
    to_quest.click()
    time.sleep(0.8)

    # friend request cancel if any
    region = (x, y+h*3//5) + (w, h//9)
    found = utility.locate(friend_cancel.path, region)
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
    w, h = window_size
    x, y = top_left
    region = (x, y+h*2//5) + (w//2, h//5)
    medal = join(images_dir, 'medal.png')
    found = utility.locate(medal, region)
    if found is not None:
        logger.info('chip dialog found')
        chips_ok.click()

def halo_dialog():
    # dimension halo if any
    # do not handle it, leave it to user
    if config['dimension halo'] == 'no':
        return

    dimension_close = Button('close.png', config['dimension close'])
    w, h = window_size
    x, y = top_left
    region = (x, y+h*2//3) + (w, h//7)
    found = utility.locate(dimension_close.path, region)
    if found is not None:
        logger.info('dimension dialog found')
        logger.info('gbf robt finished')
        sys.exit(0)
