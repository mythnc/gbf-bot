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

attack = Button('attack.png', config['attack'])
reload_ = Button('reload.png', config['reload'])
back = Button('back2.png', config['back'])
character1 = Button('character.png', config['character1'])
character2 = Button('character.png', config['character2'])
character3 = Button('character.png', config['character3'])
character4 = Button('character.png', config['character4'])
characters_map = {
    'character1': character1,
    'character2': character2,
    'character3': character3,
    'character4': character4,
}
skill1 = Button('skill.png', config['skill1'])
skill2 = Button('skill.png', config['skill2'])
skill3 = Button('skill.png', config['skill3'])
skill4 = Button('skill.png', config['skill4'])
skills_map = [
    0,
    skill1,
    skill2,
    skill3,
    skill4,
]
cell = Button('guildwars_ex_cell.png', config['cell'], False)
ex_plus = Button('guildwars_ex_plus.png', config['ex+'])
ok = Button('ok1.png')
summon = SummonSelector(config['summon name'])

script = configparser.ConfigParser()
script.read(join(package_root, 'guild_wars.ini'))


def wait_battle_start(sleep_time=0.5):
    while True:
        time.sleep(sleep_time)
        found = utility.locate(attack.path, 1/2, 1/3, 1/2, 2/3)
        if found is not None:
            return


def cast(stage):
    try:
        characters = script[stage]
    except KeyError:
        characters = []

    skill_count = 0
    n = len(characters)
    for i, character in enumerate(characters):
        characters_map[character].click()
        skills = [int(skill) for skill in characters[character].split(',')]
        for skill in skills:
            skills_map[skill].click()
            time.sleep(random.random() * 0.2)
            skill_count += 1
        if i < n - 1:
            back.click()
        time.sleep(random.random() * 0.2)
    attack.click()
    ratio = 2.5
    # TODO: attention to this 2.4 or 2.5 is good
    # If lag, set ration to 3
    time.sleep(skill_count * ratio + random.random() * 0.5)


def is_over_drive():
    if not script['over drive']:
        return

    found = utility.locate(join(images_dir, 'over_drive.png'), 1/2, 0, 1/2, 1/5,
                           confidence=0.85)
    if found is None:
        return False
    return True


# TODO: method could merge with previous one
def is_finished():
    found = utility.locate(ok.path, 0, 1/2, 1, 1/4)
    #im = utility.screenshot(0, 1/2, 1, 1/4)
    #im.save('test.png')
    if found is not None:
        return True
    return False


def activate():
    pyautogui.PAUSE = 1.5

    time.sleep(2)
    pyautogui.scroll(-10)
    logger.info('click cell')
    cell.click()
    time.sleep(0.75)
    logger.info('click ex+')
    ex_plus.click()

    # chose summon
    summon.activate()

    wait_battle_start()
    # battle start
    # round by round
    for i in range(1, 30):
        round_ = 'round ' + str(i)
        logger.info('\n' + round_)
        cast(round_)
        logger.info('reload and wait')
        reload_.click()
        time.sleep(3.5)

        if is_finished():
            break

        if i == 1 and config['assault time'] == 'yes':
            time.sleep(15)

        if is_over_drive():
            logger.info('cast over drive')
            cast('over drive')
            logger.info('reload and wait')
            reload_.click()
            time.sleep(3.5)

        if is_finished():
            break

    battle_result.activate()
