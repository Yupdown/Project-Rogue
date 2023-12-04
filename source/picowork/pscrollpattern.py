from .pspriteobject import *
from .pcamera import *
from .presource import *


class PScrollPattern(PSpriteObject):
    def __init__(self, image, z_dist):
        super().__init__(image)
        self._z_dist = z_dist

    def on_draw(self):
        t = 1 - 1 / self._z_dist

        wv = lerp(self._concatenated_position, camera._position, t)
        w = self._image.w * self._concatenated_scale.x / PIXEL_PER_UNIT
        h = self._image.h * self._concatenated_scale.y / PIXEL_PER_UNIT

        bl = camera.screen_to_world(Vector2(0, 0))
        tr = camera.screen_to_world(Vector2(get_canvas_width(), get_canvas_height()))

        bx = (wv.x - bl.x - w * 0.5) % w - w + bl.x
        n = ceil((tr.x - bx) / w)

        hp = wv.y - h * 0.5 - bl.y
        s = camera.screen_size(Vector2(w, h))
        sp = camera.screen_size(Vector2(w, hp))

        rad = radians(camera.screen_rotation(self._concatenated_rotation, t ** 2))

        for tx in range(n):
            v = camera.world_to_screen(Vector2(bx + (tx + 0.5) * w, wv.y), t ** 2)
            vp = camera.world_to_screen(Vector2(bx + (tx + 0.5) * w, wv.y - (h + hp) * 0.5), t ** 2)
            if rad != 0:
                self._image.rotate_draw(rad, floor(v.x), floor(v.y), ceil(s.x), ceil(s.y))
                self._image.clip_composite_draw(0, 0, self._image.w, 1, rad, '', floor(vp.x), floor(vp.y), ceil(sp.x), ceil(sp.y))
            else:
                self._image.draw(floor(v.x), floor(v.y), ceil(s.x), ceil(s.y))
                self._image.clip_draw(0, 0, self._image.w, 1, floor(vp.x), floor(vp.y), ceil(sp.x), ceil(sp.y))