import logging
import random
import time
import pyautogui
from . import battle_result_config as config
from . import buttons
from .components import Button

logger = logging.getLogger(__name__)

result_ok = Button('ok1.png', config['result ok'])
to_quest = Button('to_quest.png', config['to quest'])
friend_cancel = Button('cancel.png', config['friend cancel'], False)


def activate():
    pyautogui.PAUSE = 0.1
    logger.info('click result ok')
    result_ok.double_click()
    time.sleep(2 + random.random() * 0.25)
    logger.info('click to quest')
    to_quest.double_click(0)
    # friend request cancel if any
    logger.info('click friend request cancel')
    friend_cancel.click(0)
    time.sleep(random.random() * 0.25)
