from .pspriteobject import *
from .pcamera import *
from .presource import *


class PScrollPattern(PSpriteObject):
    def __init__(self, image, z_dist):
        super().__init__(image)
        self._z_dist = z_dist

    def on_draw(self):
        t = 1 - 1 / self._z_dist
        v = camera.world_to_screen(lerp(self._concatenated_position, camera._position, t))
        w = self._image.w * self._concatenated_scale.x
        h = self._image.h * self._concatenated_scale.y
        s = camera.screen_size(Vector2(w, h)) / PIXEL_PER_UNIT
        rad = radians(camera.screen_rotation(self._concatenated_rotation))
        bx = (v.x - s.x / 2) % s.x - s.x
        n = ceil((get_canvas_width() - bx) / s.x)

        for tx in range(n):
            offset = s.x * tx
            dx = bx - v.x + offset + s.x / 2
            if rad != 0:
                self._image.rotate_draw(rad, floor(v.x + dx * cos(rad)), v.y + dx * sin(rad), ceil(s.x), s.y)
            else:
                self._image.draw(floor(v.x + dx), v.y, ceil(s.x), s.y)