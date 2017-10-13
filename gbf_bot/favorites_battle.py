import logging
import random
import time
import pyautogui
from . import favorites_mission_config as config
from . import buttons, auto_battle, summon, battle_result
from .components import Button

logger = logging.getLogger(__name__)


class FavoritesBattle():
    def __init__(self):
        self.cell = Button(buttons('favorites_cell.png'),
                           config['cell'],
                           False)
        self.battle_time = int(config['battle time'])
        self.logger = logging.getLogger(__name__ + '.' 
                                        + FavoritesBattle.__name__)

    def click_cell(self):
        self.cell.double_click()
        time.sleep(random.random() * 0.25)

    def activate(self):
        pyautogui.PAUSE = 1.5

        self.logger.info('click mission')
        self.click_cell()

        # AP will be checked before before next step
        # make sure AP is enough

        # chose summon
        summon.activate()

        auto_battle.activate(self.battle_time)

        battle_result.activate()
