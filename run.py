import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys
import pyautogui

root_logger = logging.getLogger('root')
root_logger.setLevel(logging.INFO)
root_ch = logging.StreamHandler()
root_ch.setLevel(logging.INFO)
root_formatter = logging.Formatter('%(name)s:%(levelname)s:%(message)s')
root_ch.setFormatter(root_formatter)
root_logger.addHandler(root_ch)


def log_gbf():
    logger = logging.getLogger('gbf_bot')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    if not os.path.exists('log'):
        os.makedirs('log')
    fh = TimedRotatingFileHandler(os.path.join('log', 'gbf_bot.log'), 'D')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s '\
                                  '- %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)


def display_menu():
    try:
        print()
        print('1) continually play favorites top mission')
        print('2) continually play slime blasting')
        print()
        print('press CTRL-C to leave')
        print('select option: ', end='')
        return input()
    except KeyboardInterrupt:
        root_logger.info('\ngbf robot finished')
        sys.exit(0)


def activate(i):
    favorite_mission = FavoritesBattle()
    d = {'1': favorite_mission, '2': slime_blasting}

    try:
        count = 1
        while True:
            root_logger.info('\nexecution times: ' + str(count))
            d[i].activate()
            count += 1
    except KeyboardInterrupt:
        root_logger.info('gbf robot finished')
    except pyautogui.FailSafeException:
        root_logger.info('gbf robot finished')


if __name__ == '__main__':
    log_gbf()
    from gbf_bot.special_battle import FavoritesBattle
    from gbf_bot import slime_blasting
    root_logger.info('gbf robot is executing...')
    option = display_menu()
    activate(option)
