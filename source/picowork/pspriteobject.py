from .pobject import *
from .pcamera import *
from .presource import *


class PSpriteObject(PObject):
    def __init__(self, image):
        super().__init__()
        self.set_image(image)

    def on_draw(self):
        v = camera.world_to_screen(self._concatenated_position)
        w = self._image.w * self._concatenated_scale.x
        h = self._image.h * self._concatenated_scale.y
        rad = radians(camera.screen_rotation(self._concatenated_rotation))
        flip = ''
        if w < 0:
            w = abs(w)
            flip += 'h'
        if h < 0:
            h = abs(h)
            flip += 'v'
        s = camera.screen_size(Vector2(w, h)) / PIXEL_PER_UNIT
        self._image.composite_draw(rad, flip, v.x, v.y, s.x, s.y)

    def set_image(self, image):
        if type(image) is str:
            self._image = get_image(image)
        else:
            self._image = image
