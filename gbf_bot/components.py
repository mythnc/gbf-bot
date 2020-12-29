import logging
from os.path import join
import random
from typing import NamedTuple

from PIL import Image
import pyautogui

from .constants import images_dir, top_left, window_size


class Mouse:

    logger = logging.getLogger(__name__)

    @staticmethod
    def move_direction():
        d = {0: -1, 1: 1}
        return d[random.randint(0, 1)]

    @staticmethod
    def calculate_click_point(center_point, size, signed, partition=4):
        click_point = [None] * 2
        for i in range(2):
            d = 1
            if signed:
                d = Mouse.move_direction()
            random_x = random.randint(0, size[i] // partition) * d
            click_point[i] = center_point[i] + random_x
        return click_point

    @staticmethod
    def click(center_point, size, duration=0.15, signed=True, partition=4):
        point = Mouse.calculate_click_point(center_point, size, signed, partition)
        pyautogui.click(*point, duration=duration)
        Mouse.logger.debug(str(point))
        return point

    @staticmethod
    def double_click(center_point, size, duration=0.0, signed=True):
        point = Mouse.calculate_click_point(center_point, size, signed)
        pyautogui.doubleClick(*point, duration=duration)
        Mouse.logger.debug(str(point))
        return point

    @staticmethod
    def click_again() -> tuple:
        pyautogui.click(duration=0.15)
        return pyautogui.position()

    @staticmethod
    def move_to(center_point):
        pyautogui.moveTo(*center_point)
        Mouse.logger.debug(str(center_point))


class Button:
    def __init__(self, name, point=None, signed=True):
        self.path = join(images_dir, "buttons", name)
        self.image = Image.open(self.path)
        self.center_point = point
        self.signed = signed

    def click(self, duration=0.15, partition=4):
        return Mouse.click(self.center_point, self.image.size, duration, self.signed, partition=partition)

    def double_click(self, duration=0.0):
        return Mouse.double_click(self.center_point, self.image.size, duration, self.signed)

    def move_to(self):
        Mouse.move_to(self.center_point)


class Region(NamedTuple):  # pylint: disable=inherit-non-class
    left: int
    top: int
    width: int
    height: int

    def move_left_point(self, ratio) -> int:
        return self.left + int(self.width * ratio)

    def move_top_point(self, ratio) -> int:
        return self.top + int(self.height * ratio)

    def divide_width(self, divide) -> int:
        return int(self.width * divide)

    def divide_height(self, divide) -> int:
        return int(self.height * divide)


class AppWindow:
    region = Region(*top_left, *window_size)

    @staticmethod
    def screenshot(region_args: tuple):
        return pyautogui.screenshot(
            region=AppWindow.get_partical_region(region_args),
        )

    @staticmethod
    def locate_on(image, region_args: tuple, confidence=0.9):
        pyautogui.PAUSE = 0.2
        return pyautogui.locateOnScreen(
            image,
            region=AppWindow.get_partical_region(region_args),
            confidence=confidence,
        )

    @staticmethod
    def locate_center(image, region_args: tuple, confidence=0.9):
        pyautogui.PAUSE = 0.2
        return pyautogui.locateCenterOnScreen(
            image,
            region=AppWindow.get_partical_region(region_args),
            confidence=confidence,
        )

    @staticmethod
    def get_partical_region(region_args: tuple) -> tuple:
        left_move_ratio, top_move_ratio, width_divide, height_divide = region_args
        return (
            AppWindow.region.move_left_point(left_move_ratio),
            AppWindow.region.move_top_point(top_move_ratio),
            AppWindow.region.divide_width(width_divide),
            AppWindow.region.divide_height(height_divide),
        )
