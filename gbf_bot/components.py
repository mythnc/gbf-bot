from os.path import join
from PIL import Image
from .constants import images_dir
from . import utility


class Button:
    def __init__(self, name, point=None, signed=True):
        self.path = join(images_dir, "buttons", name)
        self.image = Image.open(self.path)
        self.center_point = point
        self.click_point = [None] * 2
        self.signed = signed

    def click(self, duration=0.15, click_point=None, partition=4):
        return utility.click(
            self.center_point, self.image.size, duration, click_point, self.signed, partition=partition
        )

    def double_click(self, duration=0.0, click_point=None):
        return utility.double_click(self.center_point, self.image.size, duration, click_point, self.signed)

    def move_to(self):
        utility.move_to(self.center_point)
