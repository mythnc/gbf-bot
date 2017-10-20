import pyautogui
from . import top_left, window_size

width, height = window_size
x, y = top_left


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
