import configparser
import logging
from os.path import dirname, join


logger = logging.getLogger(__name__)

package_root = dirname(__file__)
images_dir = join(package_root, "images")

config = configparser.ConfigParser()
config.read(join(package_root, "config.ini"))

d = {}
for section in config.sections():
    d[section] = {}
    for key in config[section].keys():
        item = config[section][key]
        if "," in item:
            seq = []
            for x in item.split(","):
                if x.isdigit():
                    seq.append(int(x))
                else:
                    seq.append(x)
            d[section][key] = tuple(seq)
        elif item.isdigit():
            d[section][key] = int(item)
        else:
            d[section][key] = item
logger.debug(d)

top_left = d["global"]["top left"]
window_size = d["global"]["window size"]

auto_battle_config = d["auto battle"]
battle_result_config = d["battle result"]
favorites_mission_config = d["favorites mission"]
guild_wars_config = d["guild wars"]
guild_wars_hell_config = d["guild wars hell"]
poker_config = d["poker"]
slime_blasting_config = d["slime blasting"]
summon_config = d["summon"]
