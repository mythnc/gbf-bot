import logging
import random
import time

import pyautogui

from . import auto_battle, battle_result
from .constants import favorites_mission_config as config
from .summon import SummonSelector
from .components import Button, AppWindow


class FavoritesBattle:
    def __init__(self):
        self.favorites = Button("favorites.png", config["favorites"])
        self.cell = Button("favorites_cell.png", config["cell"], False)
        self.battle_time = config["battle time"]
        self.logger = logging.getLogger(f"{__name__}.{FavoritesBattle.__name__}")
        self.summon = SummonSelector(config["summon name"])

    def click_cell(self):
        self.logger.info("click mission")
        self.cell.double_click()
        time.sleep(random.random() * 0.25)

    def activate(self):
        pyautogui.PAUSE = 1.5

        count = 1
        while True:
            self.logger.info(f"execution times: {count}")

            if count == 1:
                self.favorites_menu()

            # AP will be checked before next step
            # make sure AP is enough

            # chose summon
            self.summon.activate()

            auto_battle.activate(self.battle_time)

            battle_result.activate()

            count += 1

    def favorites_menu(self):
        self.wait_before_enter_menu()
        self.click_cell()

    def wait_before_enter_menu(self, sleep_time=0.5):
        self.logger.debug("wait before enter favorites menu")
        while True:
            time.sleep(sleep_time)
            found = AppWindow.locate_on(self.favorites.path, (0, 1 / 3, 1, 1 / 7), confidence=0.75)
            if found is not None:
                return
