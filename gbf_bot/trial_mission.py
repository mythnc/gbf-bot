import logging
import random
import time
from PIL import Image
import pyautogui

IMG_PATH = 'image/'
pyautogui.PAUSE = 1.5
DURATION = 0.15
hikari_challenge = (1822, 672)
challenge = (1833, 470)
summon = (1672, 424)
summon_ok = (1790, 693)
attack = (1803, 435)
auto = (1483, 465)
result_ok = (1672, 630)
return_ = (1671, 488)
friend_cancel = (1566, 613)
explanation_ok = (1676, 591)

def activate():
    # chose battle name
    # click twice for window choice
    point = get_click_point(hikari_challenge, 'challenge_recbutton.png')
    pyautogui.doubleClick(*point, duration=DURATION)
    logging.info('click hikari challenge ' + str(point))

    point = get_click_point(challenge, 'challenge_circlebutton.png')
    pyautogui.click(*point, duration=DURATION)
    logging.info('click challenge ' + str(point))

    # TODO
    # if no AP

    # chose summon
    time.sleep(1)
    point = get_click_point(summon, 'summon_button.png')
    pyautogui.click(*point, duration=DURATION)
    logging.info('click summon ' + str(point))

    point = get_click_point(summon_ok, 'summon_ok_button.png')
    pyautogui.click(*point, duration=DURATION)
    logging.info('click ok ' + str(point))

    # battle start
    time.sleep(5)
    point = get_click_point(attack, 'attack_button.png')
    pyautogui.click(*point, duration=DURATION)
    logging.info('click attack ' + str(point))

    time.sleep(1)
    point = get_click_point(auto, 'auto_button.png')
    pyautogui.click(*point, duration=DURATION)
    logging.info('click auto ' + str(point))

    # battle result
    time.sleep(75)
    point = get_click_point(result_ok, 'complete_ok_button.png')
    pyautogui.doubleClick(*point, duration=DURATION)
    logging.info('click result ' + str(point))

    time.sleep(2)
    point = get_click_point(return_, 'return_button.png')
    # click twice for character lb up popup
    pyautogui.doubleClick(*point)
    logging.info('click return ' + str(point))

    # friend request cancel
    point = get_click_point(friend_cancel, 'return_button.png', False)
    pyautogui.click(*point, duration=DURATION)
    logging.info('click friend request cancel ' + str(point))

    point = get_click_point(explanation_ok, 'complete_ok_button.png')
    pyautogui.click(*point)
    logging.info('click ok ' + str(point))


def get_click_point(point, image_name, could_be_negative=True):
    PARTITON = 4
    image = Image.open(IMG_PATH + image_name)

    click_point = []
    for i in range(2):
        d = 1
        if could_be_negative:
            d = get_move_dicretion()
        v = point[i] + random.randint(0, image.size[i] // PARTITON) * d
        click_point.append(v)
    return tuple(click_point)


def get_move_dicretion():
    d = {0: -1, 1: 1}
    return d[random.randint(0, 1)]
