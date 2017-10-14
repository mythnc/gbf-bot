import pyautogui


def locate(image, region, confidence=0.9):
    pyautogui.PAUSE = 0.1
    return pyautogui.locateOnScreen(image, region=region, confidence=confidence)


def locate_center(image, region, confidence=0.9):
    pyautogui.PAUSE = 0.1
    return pyautogui.locateCenterOnScreen(image, region=region,
                                          confidence=confidence)
