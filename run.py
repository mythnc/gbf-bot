from datetime import datetime
import logging
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
    ch.setLevel(logging.INFO)
    log_dir = 'log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    today = datetime.now()
    file_name = '{}.log'.format(str(today).split(' ')[0])
    fh = logging.FileHandler(os.path.join(log_dir, file_name))
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
        print('3) continually play poker')
        print('4) continually play guild wars ex+')
        print()
        print('press CTRL-C to leave')
        print('select option: ', end='')
        return input()
    except KeyboardInterrupt:
        root_logger.info('\ngbf robot finished')
        sys.exit(0)


def activate(i):
    favorite_mission = FavoritesBattle()
    d = {'1': favorite_mission, '2': slime_blasting, '3': PokerBot(),
         '4': guild_wars}

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
    from gbf_bot.favorites_battle import FavoritesBattle
    from gbf_bot import slime_blasting
    from gbf_bot import guild_wars
    from gbf_bot.casino import PokerBot
    root_logger.info('gbf robot is executing...')
    option = display_menu()
    activate(option)
