import argparse
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

parser = argparse.ArgumentParser(description="Granblue Fantasy Bot")
group = parser.add_mutually_exclusive_group()
group.add_argument("-f", "--favorites", action="store_true",
                   help="Continually play favorites top mission")
group.add_argument("-b", "--blasting", action="store_true",
                   help="Continually play slime blasting")
group.add_argument("-p", "--poker", action="store_true",
                   help="Continually play poker, default play time is 30 minutes")
group.add_argument("-g", "--guildwars", action="store_true",
                   help="Continually play guild wars extreme+")

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


def activate():
    args = parser.parse_args()
    if args.favorites:
        d = FavoritesBattle()
    elif args.blasting:
        d = slime_blasting
    elif args.poker:
        d = PokerBot()
    elif args.guildwars:
        d = guild_wars

    root_logger.info('gbf robot is executing...')
    try:
        count = 1
        while True:
            root_logger.info('\nexecution times: ' + str(count))
            d.activate(count)
            count += 1
    except KeyboardInterrupt:
        root_logger.info('gbf robot finished')
    except pyautogui.FailSafeException:
        root_logger.info('gbf robot finished')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        parser.parse_args(["-h"])
        sys.exit(0)

    log_gbf()
    from gbf_bot.favorites_battle import FavoritesBattle
    from gbf_bot import slime_blasting
    from gbf_bot import guild_wars
    from gbf_bot.casino import PokerBot

    activate()
