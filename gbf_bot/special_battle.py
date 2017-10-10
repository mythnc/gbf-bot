from abc import ABCMeta, abstractmethod
import logging
import random
import time
import pyautogui
from . import angel_halo_config, trial_mission_config
from . import buttons, auto_battle, summon, battle_result
from .components import Button

logger = logging.getLogger(__name__)


class SpecialBattleTemplate(metaclass=ABCMeta):
    @abstractmethod
    def move_to_position(self):
        pass

    def click_mission(self):
        self.battle.double_click()
        time.sleep(random.random() * 0.25)

    def click_level(self):
        self.level.click()
        time.sleep(random.random() * 0.25)

    def activate(self):
        pyautogui.PAUSE = 1.5

        self.logger.info('move to position')
        self.move_to_position()
        self.logger.info('click mission')
        self.click_mission()
        self.logger.info('click level')
        self.click_level()

        # AP will be checked before before next step
        # make sure AP is enough

        # chose summon
        summon.activate()

        auto_battle.activate(self.battle_time)

        battle_result.activate()


class AngelHalo(SpecialBattleTemplate):
    def __init__(self):
        config = angel_halo_config
        self.battle = Button(buttons('select.png'), config['angel_halo'])
        self.level = Button(buttons('play.png'), config['angel_halo_level'])
        self.battle_time = int(config['battle_time'])
        self.logger = logging.getLogger(__name__ + '.' + AngelHalo.__name__)

    def move_to_position(self):
        self.battle.move_to()
        self.logger.info('scroll mouse to the bottom')
        pyautogui.scroll(-30)


class TrialMission(SpecialBattleTemplate):
    def __init__(self):
        config = trial_mission_config
        self.battle = Button(buttons('select.png'), config['trial'])
        self.level = Button(buttons('play.png'), config['trial_level'])
        self.battle_time = int(config['battle_time'])
        self.logger = logging.getLogger(__name__ + '.' + TrialMission.__name__)

    def move_to_position(self):
        # TODO: position changes by days
        pass
