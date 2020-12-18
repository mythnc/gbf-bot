import configparser
import logging
from os.path import join
import random
import time
import pyautogui
from .constants import package_root, images_dir, guild_wars_config as config
from . import utility, battle_result
from .summon import SummonSelector
from .components import Button


logger = logging.getLogger(__name__)

attack = Button("attack.png", config["attack"])
reload_ = Button("reload.png", config["reload"])
back = Button("back2.png", config["back"])
character1 = Button("character.png", config["character1"])
character2 = Button("character.png", config["character2"])
character3 = Button("character.png", config["character3"])
character4 = Button("character.png", config["character4"])
characters_map = {
    "character1": character1,
    "character2": character2,
    "character3": character3,
    "character4": character4,
}
skill1 = Button("skill.png", config["skill1"])
skill2 = Button("skill.png", config["skill2"])
skill3 = Button("skill.png", config["skill3"])
skill4 = Button("skill.png", config["skill4"])
skills_map = [
    0,
    skill1,
    skill2,
    skill3,
    skill4,
]

battle_summon_list = Button("battle_summon_list.png", config["battle summon list"])
battle_summon1 = Button("battle_summon_list.png", config["battle summon 1"])
battle_summon2 = None
battle_summon3 = None
battle_summon4 = None
battle_summon5 = None
battle_summon6 = Button("battle_summon_list.png", config["battle summon 6"])
summons_map = [
    0,
    battle_summon1,
    battle_summon2,
    battle_summon3,
    battle_summon4,
    battle_summon5,
    battle_summon6,
]
battle_summon_confirm = Button("ok3.png", config["battle summon confirm"])


cell = Button("guildwars_ex_cell.png", config["cell"], False)
ex_plus = Button("guildwars_ex_plus.png", config["ex+"])
ok = Button("ok1.png")
summon = SummonSelector(config["summon name"])

script = configparser.ConfigParser()
script.read(join(package_root, "guild_wars.ini"))

auto = Button("auto.png", config["auto"])


def wait_battle_start(sleep_time=0.5):
    while True:
        time.sleep(sleep_time)
        found = utility.locate(attack.path, 1 / 2, 1 / 3, 1 / 2, 2 / 3)
        if found is not None:
            return


def cast(stage):
    try:
        commands = script[stage]
    except KeyError:
        commands = []

    skill_count = 0
    n = len(commands)
    for i, command in enumerate(commands):
        if "character" in command:
            skill_count += use_character(command, commands[command])
        elif "summon" == command:
            use_summon(int(commands[command]))
            skill_count += 1

        if i < n - 1 and "character" in command:
            back.click()
        time.sleep(random.random() * 0.2)
    attack.click()
    # ratio = 2.4
    # TODO: attention to this 2.4 or 2.5 is good
    # If lag, set ration to 3
    # time.sleep(skill_count * ratio + random.random() * 0.5)


def use_character(character, behavior):
    characters_map[character].click()
    skills = [int(skill) for skill in behavior.split(",")]
    count = 0
    for skill in skills:
        skills_map[skill].click()
        time.sleep(random.random() * 0.2)
        count += 1
    return count


def use_summon(number):
    battle_summon_list.click()
    summons_map[number].click()
    battle_summon_confirm.click(partition=8)
    time.sleep(random.random() * 0.2)


def is_over_drive():
    if not script["over drive"]:
        return

    found = utility.locate(join(images_dir, "over_drive.png"), 1 / 2, 0, 1 / 2, 1 / 5, confidence=0.85)
    if found is None:
        return False
    return True


# TODO: method could merge with previous one
def is_finished():
    found = utility.locate(ok.path, 0, 1 / 2, 1, 1 / 4)
    # im = utility.screenshot(0, 1/2, 1, 1/4)
    # im.save('test.png')
    if found is not None:
        return True
    return False


def activate(count):
    pyautogui.PAUSE = 1.5

    # chose enemy
    if count == 1:
        time.sleep(1)
        pyautogui.click(1671, 232)
        pyautogui.scroll(-10)
        logger.info("click cell")
        cell.click(partition=8)
        time.sleep(0.75)
        logger.info("click ex+")
        ex_plus.click(partition=10)

    # chose summon
    summon.activate(True)

    wait_battle_start()
    # battle start
    # round by round
    for times in range(1, 6):
        round_ = "round " + str(times)
        logger.info("\n" + round_)
        cast(round_)

        # click auto
        if times == 1:
            # logger.info('click auto')
            # auto.click(partition=12)
            time.sleep(20 + random.random() * 0.2)
        elif times == 2:
            logger.info("wait 10 sec")
            time.sleep(15)
        else:
            time.sleep(2)

        reload_.click()
        # time.sleep(3)
        time.sleep(4)

        if is_finished():
            break

        if times == 1 and config["assault time"] == "yes":
            time.sleep(15)

        if is_over_drive():
            logger.info("cast over drive")
            cast("over drive")
            logger.info("reload and wait")
            reload_.click()
            time.sleep(3.5)

        if is_finished():
            break

    battle_result.activate()
