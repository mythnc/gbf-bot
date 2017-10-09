import logging
import random
import time
import pyautogui
from . import buttons
from . import summon_config as config
from .components import Button

logger = logging.getLogger(__name__)

summon = Button(buttons('summon.png'), config['summon'])
summon_ok = Button(buttons('ok2.png'), config['summon_ok'])


def activate():
    pyautogui.PAUSE = 1.5
    time.sleep(1)
    logger.info('click summon')
    summon.click()
    time.sleep(random.random() * 0.25)
    logger.info('click ok')
    summon_ok.click()
