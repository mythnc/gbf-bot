import logging
import random
import time
import pyautogui
from .constants import slime_blasting_config as config
from .components import Button

logger = logging.getLogger(__name__)

start = Button('start.png', config['start'])
character1 = Button('character.png', config['character1'])
skill = Button('skill.png', config['skill'])
back = Button('back.png', config['back'])


def activate():
    logger.info('slime blasting start')
    pyautogui.PAUSE = 1.2
    # click twice for window choice
    logger.info('click start')
    start.double_click()

    # AP will be checked before next step
    # make sure AP is enough

    time.sleep(5 + random.random() * 0.5)
    logger.info('click character')
    character1.double_click()
    time.sleep(random.random() * 0.25)
    logger.info('click skill')
    skill.click()
    time.sleep(random.random() * 0.25)
    logger.info('click back')
    back_point = back.click()
    time.sleep(1 + random.random() * 0.25)

    # battle result
    logger.info('click back')
    back.click(0, back_point)
    time.sleep(random.random() * 0.25)
    logger.info('slime blasting end')
