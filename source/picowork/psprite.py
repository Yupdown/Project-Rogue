from pico2d import *
from .presource import *


class PSprite:
    def __init__(self, image, x, y, w, h):
        if type(image) is str:
            self._image = get_image(image)
        else:
            self._image = image
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, x, y, w = None, h = None):
        self.composite_draw(0, '', x, y, w, h)

    def rotate_draw(self, rad, x, y, w = None, h = None):
        self.composite_draw(rad, '', x, y, w, h)

    def composite_draw(self, rad, flip, x, y, w = None, h = None):
        self._image.clip_composite_draw(self.x, self.y, self.w, self.h, rad, flip, x, y, w, h)