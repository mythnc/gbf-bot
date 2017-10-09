import logging
import random
import time
import pyautogui
from . import slime_blasting_config as config
from . import buttons
from .components import Button

logger = logging.getLogger(__name__)

start = Button(buttons('start.png'), config['start'])
character1 = Button(buttons('character.png'), config['character1'])
skill = Button(buttons('skill.png'), config['skill'])
back = Button(buttons('back.png'), config['back'])


def activate():
    logger.info('slime blasting start')
    pyautogui.PAUSE = 1.2
    # click twice for window choice
    logger.info('click start')
    start.double_click()

    # AP will be checked before next step
    # make sure AP is enough

    time.sleep(5 + random.random() * 0.25)
    logger.info('click character')
    character1.double_click()
    logger.info('click skill')
    skill.click()
    time.sleep(random.random() * 0.25)
    logger.info('click back')
    back.click()
    time.sleep(random.random() * 0.25)

    # battle result
    logger.info('click back')
    back.click(0)
    time.sleep(random.random() * 0.25)
    logger.info('slime blasting end')
