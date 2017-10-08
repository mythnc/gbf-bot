import logging
import random
from PIL import Image
import pyautogui

logger = logging.getLogger(__name__)


class Button:
    def __init__(self, image_path, point, signed=True):
        self.image = Image.open(image_path)
        self.center_point = point
        self.click_point = [None] * 2
        self.signed = signed
        self.logger = logging.getLogger('gbf_bot.components.Button')

    def calculate_click_point(self, partition=4):
        for i in range(2):
            d = 1
            if self.signed:
                d = self.move_direction()
            random_x = random.randint(0, self.image.size[i] // partition) * d
            self.click_point[i] = self.center_point[i] + random_x

    def move_direction(self):
        d = {0: -1, 1: 1}
        return d[random.randint(0, 1)]

    def click(self, duration=0.15):
        self.calculate_click_point()
        pyautogui.click(*self.click_point, duration=duration)
        self.logger.info(str(self.click_point))

    def double_click(self, duration=0.15):
        self.calculate_click_point()
        pyautogui.doubleClick(*self.click_point, duration=duration)
        self.logger.info(str(self.click_point))
