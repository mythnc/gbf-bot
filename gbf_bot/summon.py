import logging
from os.path import join
import time
import pyautogui
from . import buttons, package_root
from .components import Button

logger = logging.getLogger(__name__)

points = {}
with open(join(package_root, 'summon_points')) as f:
    exec(f.read(), points)

summon = Button(buttons('summon.png'), points['summon'])
summon_ok = Button(buttons('ok2.png'), points['summon_ok'])


def activate():
    pyautogui.PAUSE = 1.5
    time.sleep(1)
    logger.info('click summon')
    summon.click()
    logger.info('click ok')
    summon_ok.click()
