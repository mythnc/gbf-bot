import logging
from os.path import join
import random
import sys
import time
import pyautogui
from .constants import images_dir, summon_config as config
from . import utility
from .components import Button

logger = logging.getLogger(__name__)

summon_dir = join(images_dir, "summons")
summon_mapping = {
    "hint": join(summon_dir, "hint.png"),
    # fire
    "athena": join(summon_dir, "athena.png"),
    "colossus omega": join(summon_dir, "colossus_omega.png"),
    "colossus omega 4s": join(summon_dir, "colossus_omega_4s.png"),
    "shiva": join(summon_dir, "shiva.png"),
    # water
    "leviathan omega": join(summon_dir, "leviathan_omega.png"),
    "europa": join(summon_dir, "europa.png"),
    "macula marius": join(summon_dir, "macula_marius.png"),
    "varuna": join(summon_dir, "varuna.png"),
    # earth
    "baal": join(summon_dir, "baal.png"),
    "medusa": join(summon_dir, "medusa.png"),
    "godsworn alexiel": join(summon_dir, "godsworn_alexiel.png"),
    "tezcatlipoca": join(summon_dir, "tezcatlipoca.png"),
    # light
    "apollo": join(summon_dir, "apollo.png"),
    "lucifer": join(summon_dir, "lucifer.png"),
    # dark
    "odin": join(summon_dir, "odin.png"),
    "bahamut": join(summon_dir, "bahamut.png"),
    "celeste omega": join(summon_dir, "celeste_omega.png"),
    "dark angel olivia": join(summon_dir, "dark_angel_olivia.png"),
    # drop rates
    "kaguya": join(summon_dir, "kaguya.png"),
    "white rabbit": join(summon_dir, "white_rabbit.png"),
    # special
    "huanglong": join(summon_dir, "huanglong.png"),
}


class SummonSelector:
    cell_interval = 129
    # from image center to cell center
    image_to_cell = (160, -13)
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
    def find(name):
        image = summon_mapping[name]
        for _ in range(3):
            point = utility.locate_center(image, 0, 0, 1 / 3, 1)
            if point is not None:
                SummonSelector.logger.info(name + " found")
                return [p + move for p, move in zip(point, SummonSelector.image_to_cell)]
            # if using keyboard space, gbf window have to be selected first
            # on the other hand, mouse scroll doesn't have to be.
            pyautogui.scroll(-20)

        # if not found
        pyautogui.scroll(60)
        return None

    def activate(self, bot_detect=False):
        # wait before summon page is ready
        count = 0
        while True:
            time.sleep(0.5)
            if self.is_guild_wars and count % 10 == 0:
                self.logger.debug("click again")
                utility.click()
            image = summon_mapping["hint"]
            hint = utility.locate(image, 0, 0, 1, 1 / 3)
            if hint is not None:
                self.logger.info("enter summon page")
                break
            count += 1
        time.sleep(random.random() * 0.25)

        if bot_detect:
            confirm_img = join(images_dir, "auth_confirm.png")
            confirm_dialog = utility.locate(confirm_img, 0, 0, 1, 1)
            if confirm_dialog is not None:
                for _ in range(10):
                    self.logger.info(">>>> CLICK IT NOW <<<<")
                sys.exit(0)

        # find summon
        start = time.time()
        for name in self.names:
            point = self.find(name)
            if point is not None:
                break
        end = time.time()
        self.logger.debug("summon search time: {:.2f} sec".format(end - start))

        if point is None:
            self.logger.info("No " + str(self.names))
            self.logger.info("Random choose one from top 3 summons")
            x, y = SummonSelector.first_summon_pt
            index = random.randint(0, 2)
            point = (x, y + SummonSelector.cell_interval * index)

        self.logger.info("click selected summon")
        self.summon.center_point = point
        self.summon.double_click()
        time.sleep(random.random() * 0.25)

        # wait before confirm dialog popup
        while True:
            time.sleep(0.5)
            dialog = utility.locate(SummonSelector.dialog_ok.path, 1 / 3, 2 / 3, 2 / 3, 1 / 3)
            if dialog is not None:
                self.logger.info("dialog popped up")
                break

        self.logger.info("click ok")
        SummonSelector.dialog_ok.click()
