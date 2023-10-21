from .pobject import *
from . import presource


class PSpriteObject(PObject):
    def __init__(self, file_name):
        super().__init__()
        self._image = presource.get_image(file_name)

    def on_draw(self):
        rad = radians(self._concatenated_rotation)
        w = self._image.w * self._concatenated_scale.x
        h = self._image.h * self._concatenated_scale.y
        self._image.rotate_draw(rad, self._concatenated_position.x, self._concatenated_position.y, w, h)
