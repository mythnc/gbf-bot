import logging
from os.path import join
import random
import sys
import time

import pyautogui

from .constants import images_dir, summon_config as config
from .components import Button, AppWindow, Mouse


class SummonSelector:
    dialog_ok = Button("ok2.png", config["dialog ok"])
    first_summon_pt = config["first summon cell"]
    logger = logging.getLogger(__name__ + "." + "SummonSelector")

    def __init__(self, names, is_guild_wars=False):
        self.names = names
        self.logger = logging.getLogger(__name__ + "." + SummonSelector.__name__)
        # default summon is the top 1
        self.summon = Button("summon_cell.png", SummonSelector.first_summon_pt)
        self.is_guild_wars = is_guild_wars

    @staticmethod
    def compare(name: str):
        image = SummonSelector.get_summon_image_path(name)
        scroll_times = 3
        scroll_length = 20
        for _ in range(scroll_times):
            # XXX: width divide need to update?
            point = AppWindow.locate_center(image, (0, 0, 1 / 3, 1))
            if point is not None:
                SummonSelector.logger.info(f"found: {name}")
                # move point from image center to cell center before return
                image_to_cell = (160, -13)
                return [loc + move_length for loc, move_length in zip(point, image_to_cell)]

            # Mouse scroll could use directly without selecting app first
            # But if using keyboard space key, app have to be selected first
            pyautogui.scroll(-scroll_length)

        # if not found
        pyautogui.scroll(scroll_length * scroll_times)
        return None

    @staticmethod
    def get_summon_image_path(name: str) -> str:
        """Naming should follow rule, or there is no image path"""
        return join(images_dir, "summons", f"{name.replace(' ', '_')}.png")

    # XXX: refactor - remove flag parameter
    def activate(self, bot_detect=False):
        # wait before summon page is ready
        count = 0
        while True:
            time.sleep(0.5)
            if self.is_guild_wars and count % 10 == 0:
                self.logger.debug("click again")
                Mouse.click_again()
            image = self.get_summon_image_path("hint")
            hint = AppWindow.locate_on(image, (0, 0, 1, 1 / 3))
            if hint is not None:
                self.logger.info("enter summon page")
                break
            count += 1
        time.sleep(random.random() * 0.25)

        if bot_detect:
            confirm_img = join(images_dir, "auth_confirm.png")
            confirm_dialog = AppWindow.locate_on(confirm_img, (0, 0, 1, 1))
            if confirm_dialog is not None:
                for _ in range(10):
                    self.logger.info(">>>> CLICK IT NOW <<<<")
                sys.exit(0)

        self.summon.center_point = self.find_summon_point()
        self.logger.info("click selected summon")
        self.summon.double_click()
        time.sleep(random.random() * 0.25)

        self.wait_dialog_box()

        self.logger.info("click ok")
        SummonSelector.dialog_ok.click()

    def wait_dialog_box(self):
        """Wait before confirm dialog box popup"""
        while True:
            time.sleep(0.5)
            dialog = AppWindow.locate_on(SummonSelector.dialog_ok.path, (1 / 3, 2 / 3, 2 / 3, 1 / 3))
            if dialog is not None:
                self.logger.info("dialog popped up")
                return

    def find_summon_point(self) -> tuple:
        """
        Find summon by using `self.names`.
        If there are no summons, random chose one from top 3 summons.
        """
        for name in self.names:
            point = self.compare(name)
            if point is not None:
                return point

        self.logger.info(f"No {self.names}")
        self.logger.info("Random choose one from top 3 summons")
        return self.random_chose_summon(3)

    @staticmethod
    def random_chose_summon(summon_index: int) -> tuple:
        x, y = SummonSelector.first_summon_pt
        index = random.randint(0, summon_index - 1)
        cell_interval = 129
        return (x, y + cell_interval * index)
