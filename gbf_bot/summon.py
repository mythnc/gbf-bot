import logging
from os.path import join
import time
import pyautogui
from . import buttons, package_root
from . import summon_config as points
from .components import Button

logger = logging.getLogger(__name__)

summon = Button(buttons('summon.png'), points['summon'])
summon_ok = Button(buttons('ok2.png'), points['summon_ok'])


def activate():
    pyautogui.PAUSE = 1.5
    time.sleep(1)
    logger.info('click summon')
    summon.click()
    logger.info('click ok')
    summon_ok.click()
