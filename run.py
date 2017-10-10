import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys
import pyautogui

root_logger = logging.getLogger('root')
root_logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s:%(levelname)s:%(message)s')
ch.setFormatter(formatter)
root_logger.addHandler(ch)


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
        print('1) continually play angel halo')
        print('2) continually play slime blasting')
        print('3) continually play trial mission')
        print()
        print('press CTRL-C to leave')
        print('select option: ', end='')
        return input()
    except KeyboardInterrupt:
        root_logger.info('\ngbf robot finished')
        sys.exit(0)


def activate(i):
    angel_halo = AngelHalo()
    trial_mission = TrialMission()
    d = {'1': angel_halo, '2': slime_blasting, '3': trial_mission}

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
    from gbf_bot.special_battle import AngelHalo, TrialMission
    from gbf_bot import slime_blasting
    root_logger.info('gbf robot is executing...')
    i = display_menu()
    activate(i)
