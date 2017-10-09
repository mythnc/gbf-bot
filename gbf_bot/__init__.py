import configparser
import logging
from os.path import dirname, join

__all__ = []

logger = logging.getLogger(__name__)

package_root = dirname(__file__)
images_dir = join(package_root, 'images')
buttons = lambda x: join(images_dir, 'buttons', x)

config = configparser.ConfigParser()
config.read(join(package_root, 'config.ini'))

d = {}
for section in config.sections():
    d[section] = {}
    for key in config[section].keys():
        item = config[section][key]
        if ',' in item:
            d[section][key] = tuple([int(x) for x in item.split(',')])
        else:
            d[section][key] = item
logger.debug(d)

angel_halo_config = d['angel halo']
auto_battle_config = d['auto battle']
battle_result_config = d['battle result']
slime_blasting_config = d['slime blasting']
summon_config = d['summon']
trial_mission_config = d['trial mission']
