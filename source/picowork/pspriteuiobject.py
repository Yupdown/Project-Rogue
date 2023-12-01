from .pobject import *
from .presource import *


UI_SCALE_MULTIPLY = 4


class PSpriteUIObject(PObject):
    def __init__(self, image):
        super().__init__()
        self.set_image(image)

    def on_draw(self):
        v = self._concatenated_position
        w = self._image.w * self._concatenated_scale.x * UI_SCALE_MULTIPLY
        h = self._image.h * self._concatenated_scale.y * UI_SCALE_MULTIPLY
        rad = radians(self._concatenated_rotation)
        flip = ''
        if w < 0:
            w = abs(w)
            flip += 'h'
        if h < 0:
            h = abs(h)
            flip += 'v'
        self._image.composite_draw(rad, flip, v.x, v.y, w, h)

    def set_image(self, image):
        if type(image) is str:
            self._image = get_image(image)
        else:
            self._image = image
