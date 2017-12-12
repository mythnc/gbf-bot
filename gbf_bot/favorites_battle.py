import logging
import random
import time
import pyautogui
from . import auto_battle, battle_result, utility
from .constants import favorites_mission_config as config
from .summon import SummonSelector
from .components import Button


class FavoritesBattle():
    def __init__(self):
        self.favorites = Button('favorites.png', config['favorites'])
        self.cell = Button('favorites_cell.png',
                           config['cell'],
                           False)
        self.battle_time = config['battle time']
        self.logger = logging.getLogger(__name__ + '.'
                                        + FavoritesBattle.__name__)
        self.summon = SummonSelector(config['summon name'])

    def click_cell(self):
        self.cell.double_click()
        time.sleep(random.random() * 0.25)

    def activate(self):
        pyautogui.PAUSE = 1.5

        # wait before enter favorites menu
        self.logger.debug('wait before enter favorites menu')
        while True:
            time.sleep(0.5)
            found = utility.locate(self.favorites.path, 0, 1/3, 1, 1/7,
                                   confidence=0.75)
            if found is not None:
                break

        self.logger.info('click mission')
        self.click_cell()

        # AP will be checked before before next step
        # make sure AP is enough

        # chose summon
        self.summon.activate()

        auto_battle.activate(self.battle_time)

        battle_result.activate()
