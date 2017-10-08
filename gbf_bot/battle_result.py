import logging
from os.path import join
import time
import pyautogui
from . import battle_result_config as points
from . import buttons, package_root
from .components import Button

logger = logging.getLogger(__name__)

result_ok = Button(buttons('ok1.png'), points['result_ok'])
to_quest = Button(buttons('to_quest.png'), points['to_quest'])
friend_cancel = Button(buttons('cancel.png'), points['friend_cancel'], False)

def activate():
    pyautogui.PAUSE = 0.1
    logger.info('click result ok')
    result_ok.double_click()
    time.sleep(2)
    logger.info('click to quest')
    to_quest.double_click(0)
    # friend request cancel if any
    logger.info('click friend request cancel')
    friend_cancel.click(0)
