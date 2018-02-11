import logging
import random
import pyautogui
from .constants import top_left, window_size

logger = logging.getLogger(__name__)

width, height = window_size
x, y = top_left


def move_direction():
    d = {0: -1, 1: 1}
    return d[random.randint(0, 1)]


def calculate_click_point(center_point, size, signed, partition=4):
    click_point = [None] * 2
    for i in range(2):
        d = 1
        if signed:
            d = move_direction()
        random_x = random.randint(0, size[i] // partition) * d
        click_point[i] = center_point[i] + random_x
    return click_point


def click(center_point=None, size=None, duration=0.15, click_point=None,
          signed=True, behavior=pyautogui.click, partition=4):
    if center_point is None and size is None:
        behavior(duration=duration)
        return pyautogui.position()

    point = click_point
    if point is None:
        point = calculate_click_point(center_point, size, signed, partition)
    behavior(*point, duration=duration)
    logger.debug(str(point))
    return point


def double_click(center_point, size, duration=0.0, click_point=None, signed=True):
    return click(center_point, size, duration, click_point, signed,
                 pyautogui.doubleClick)


def move_to(center_point):
    pyautogui.moveTo(*center_point)
    logger.debug(str(center_point))


def display_pause():
    print(pyautogui.PAUSE)


def locate(image, *args, confidence=0.9, behavior=pyautogui.locateOnScreen):
    pyautogui.PAUSE = 0.2
    x_move_ratio, y_move_ratio, width_divide, height_divide = args
    start_point = (x + int(width * x_move_ratio),
                   y + int(height * y_move_ratio))
    size = (int(width * width_divide), int(height * height_divide))
    region = start_point + size
    return behavior(image, region=region, confidence=confidence)


def locate_center(image, *args, confidence=0.9):
    return locate(image, *args, confidence=confidence,
                  behavior=pyautogui.locateCenterOnScreen)


def screenshot(*args):
    x_move_ratio, y_move_ratio, width_divide, height_divide = args
    start_point = (x + int(width * x_move_ratio),
                   y + int(height * y_move_ratio))
    size = (int(width * width_divide), int(height * height_divide))
    region = start_point + size
    return pyautogui.screenshot(region=region)
