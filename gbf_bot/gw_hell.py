import logging
import random
import time

import pyautogui

from . import auto_battle, battle_result
from .constants import guild_wars_hell_config as config
from .summon import SummonSelector
from .components import Button


class GuildWarsHell:
    def __init__(self):
        self.cell = Button("guildwars_ex_cell.png", config["cell"], False)
        self.ok = Button("ok4.png", config["ok"], False)
        self.battle_time = config["battle time"]
        self.logger = logging.getLogger(f"{__name__}.{GuildWarsHell.__name__}")
        self.summon = SummonSelector(config["summon name"])

    def click_cell(self):
        self.logger.info("click hell")
        self.cell.double_click()
        time.sleep(random.random() * 0.25)
        self.ok.click()
        time.sleep(random.random() * 0.25)

    def activate(self):
        pyautogui.PAUSE = 1.5

        count = 1
        while True:
            self.logger.info(f"execution times: {count}")

            if count == 1:
                self.click_cell()

            # AP will be checked before next step
            # make sure AP is enough

            # chose summon
            self.summon.activate()

            auto_battle.activate(self.battle_time)

            battle_result.activate()

            count += 1
