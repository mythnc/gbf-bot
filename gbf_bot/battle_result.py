import logging
import random
import time
import pyautogui
from . import top_left, window_size
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

    # if De La Fille (Earth) in the party
    # there is chance casino chips dialog will be popped up

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

    # dimension halo if any
