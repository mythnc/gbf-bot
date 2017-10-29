import logging
from os.path import join
from PIL import Image
from . import images_dir
from . import utility

logger = logging.getLogger(__name__)


class Button:
    def __init__(self, name, point, signed=True):
        self.path = join(images_dir, 'buttons', name)
        self.image = Image.open(self.path)
        self.center_point = point
        self.click_point = [None] * 2
        self.signed = signed
        self.logger = logging.getLogger(__name__ + '.' + Button.__name__)

    def click(self, duration=0.15, click_point=None):
        return utility.click(self.center_point, self.image.size, duration,
                             click_point, self.signed)

    def double_click(self, duration=0.0, click_point=None):
        return utility.double_click(self.center_point, self.image.size, duration,
                                    click_point, self.signed)

    def move_to(self):
        utility.move_to(self.center_point)
