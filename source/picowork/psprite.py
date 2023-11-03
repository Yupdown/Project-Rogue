from pico2d import *


class PSprite:
    def __init__(self, image: pico2d.Image, x, y, w, h):
        self._image = image
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, x, y, w = None, h = None):
        self._image.clip_draw(self.x, self.y, self.w, self.h, x, y, w, h)

    def rotate_draw(self, rad, x, y, w = None, h = None):
        self._image.clip_composite_draw(self.x, self.y, self.w, self.h, rad, '', x, y, w, h)