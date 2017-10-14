import logging
from os.path import join
import random
import time
import pyautogui
from . import images_dir, top_left, window_size
from . import summon_config as config
from . import utility
from .components import Button

logger = logging.getLogger(__name__)

summon_dir = join(images_dir, 'summons')
summon_mapping = {
    'hint': join(summon_dir, 'hint.png'),
    'kaguya': join(summon_dir, 'kaguya.png'),
    'white rabbit': join(summon_dir, 'white_rabbit.png'),
}


class SummonSelector:
    cell_interval = 129
    # from image center to cell center
    image_to_cell = (160, -13)
    dialog_ok = Button('ok2.png', config['dialog ok'])
    first_summon_pt = config['first summon cell']
    logger = logging.getLogger(__name__ + '.' + 'SummonSelector')

    def __init__(self, names):
        self.names = names
        self.logger = logging.getLogger(__name__ + '.' + SummonSelector.__name__)
        # default summon is the top 1
        self.summon = Button('summon_cell.png',
                             SummonSelector.first_summon_pt)

    @staticmethod
    def find(name):
        image = summon_mapping[name]
        w, h = window_size
        region = top_left + (w//3, h)
        for _ in range(3):
            point = utility.locate_center(image, region)
            if point is not None:
                SummonSelector.logger.info(name + ' found')
                return [p + move for p, move in zip(point, SummonSelector.image_to_cell)]
            # if using keyboard space, gbf window have to be selected first
            # on the other hand, mouse scroll doesn't have to be.
            pyautogui.scroll(-20)

        # if not found
        pyautogui.scroll(60)
        return None

    def activate(self):
        # wait before summon page is ready
        w, h = window_size
        region = top_left + (w, h//3)
        while True:
            time.sleep(0.5)
            image = summon_mapping['hint']
            hint = utility.locate(image, region)
            if hint is not None:
                self.logger.info('enter summon page')
                break
        time.sleep(random.random() * 0.25)

        # find summon
        start = time.time()
        for name in self.names:
            point = self.find(name)
            if point is not None:
                break
        end = time.time()
        self.logger.debug('summon search time: {:.2f} sec'.format(end-start))


        if point is None:
            self.logger.info('No ' + str(self.names))
            self.logger.info('Random choose one from top 3 summons')
            x, y = SummonSelector.first_summon_pt
            index = random.randint(0, 2)
            point = (x, y + SummonSelector.cell_interval * index)

        logger.info('click selected summon')
        self.summon.center_point = point
        self.summon.double_click()
        time.sleep(random.random() * 0.25)

        # wait before confirm dialog popup
        w, h = window_size
        start_pt = (top_left[0], top_left[1] + h*2//3)
        region = start_pt + (w, h//3)
        while True:
            time.sleep(0.5)
            dialog = utility.locate(SummonSelector.dialog_ok.path, region)
            if dialog is not None:
                self.logger.info('dialog popped up')
                break

        logger.info('click ok')
        SummonSelector.dialog_ok.click()
