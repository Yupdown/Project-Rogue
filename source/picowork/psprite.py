from pico2d import *


class PSprite:
    def __init__(self, image: pico2d.Image, x, y, w, h):
        self._image = image
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def draw(self, x, y, w = None, h = None):
        self._image.clip_draw(self._x, self._y, self._w, self._h, x, y, w, h)

    def rotate_draw(self, rad, x, y, w = None, h = None):
        self._image.clip_composite_draw(self._x, self._y, self._w, self._h, rad,False, x, y, w, h)