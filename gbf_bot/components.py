import logging
from os.path import join
import random
from PIL import Image
import pyautogui
from . import images_dir

logger = logging.getLogger(__name__)


class Button:
    def __init__(self, name, point, signed=True):
        self.path = join(images_dir, 'buttons', name)
        self.image = Image.open(self.path)
        self.center_point = point
        self.click_point = [None] * 2
        self.signed = signed
        self.logger = logging.getLogger(__name__ + '.' + Button.__name__)

    def calculate_click_point(self, partition=4):
        for i in range(2):
            d = 1
            if self.signed:
                d = self.move_direction()
            random_x = random.randint(0, self.image.size[i] // partition) * d
            self.click_point[i] = self.center_point[i] + random_x

    @staticmethod
    def move_direction():
        d = {0: -1, 1: 1}
        return d[random.randint(0, 1)]

    def click(self, duration=0.15, click_point=None, click=pyautogui.click):
        if click_point is None:
            self.calculate_click_point()
        else:
            self.click_point = click_point
        click(*self.click_point, duration=duration)
        self.logger.info(str(self.click_point))
        return self.click_point

    def double_click(self, duration=0.15, click_point=None):
        return self.click(duration, click_point, pyautogui.doubleClick)

    def move_to(self):
        pyautogui.moveTo(*self.center_point)
        self.logger.info(str(self.center_point))

    @staticmethod
    def display_pause():
        print(pyautogui.PAUSE)
