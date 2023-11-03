from .pobject import *
from .pcamera import *
from .presource import *

class PSpriteObject(PObject):
    def __init__(self, image):
        super().__init__()
        if type(image) is str:
            self._image = get_image(image)
        else:
            self._image = image

    def on_draw(self):
        v = camera.world_to_screen(self._concatenated_position)
        w = self._image.w * self._concatenated_scale.x
        h = self._image.h * self._concatenated_scale.y
        s = camera.screen_size(Vector2(w, h)) / PIXEL_PER_UNIT
        rad = radians(camera.screen_rotation(self._concatenated_rotation))
        if rad != 0:
            self._image.rotate_draw(rad, v.x, v.y, s.x, s.y)
        else:
            self._image.draw(v.x, v.y, s.x, s.y)
