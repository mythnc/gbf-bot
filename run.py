import argparse
import logging
import sys

from gbf_bot.favorites_battle import FavoritesBattle
from gbf_bot import slime_blasting
from gbf_bot import guild_wars
from gbf_bot.casino import PokerBot
from gbf_bot.gw_hell import GuildWarsHell


logger = logging.getLogger(__name__)


def set_arguments(parser: argparse.ArgumentParser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--favorites", action="store_true", help="Continually play favorites top mission")
    group.add_argument("-b", "--blasting", action="store_true", help="Continually play slime blasting")
    group.add_argument("-p", "--poker", action="store_true", help="Continually play poker, default play time is 30 minutes")
    group.add_argument("-g", "--guildwars", action="store_true", help="Continually play guild wars extreme+")
    group.add_argument("-e", "--gwhell", action="store_true", help="Continually play guild wars hell")

def get_mode(args: argparse.Namespace):
    mode_map = {
        "favorites": FavoritesBattle(),
        "blasting": slime_blasting,
        "poker": PokerBot(),
        "guildwars": guild_wars,
        "gwhell": GuildWarsHell(),
    }
    for key, value in vars(args).items():
        if value:
            return mode_map[key]
    return None


def activate(mode):
    logger.info("gbf robot is executing...")
    try:
        mode.activate()
    finally:
        logger.info("gbf robot finished")


def check_argument(parser):
    if len(sys.argv) == 1:
        parser.parse_args(["-h"])
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Granblue Fantasy Bot")
    set_arguments(parser)
    check_argument(parser)

    activate(get_mode(parser.parse_args()))


if __name__ == "__main__":
    main()
