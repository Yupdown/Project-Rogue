from .pobject import *
from .pcamera import *
from .presource import *


class PTileMapObject(PObject):
    def __init__(self, w, h, s):
        super().__init__()
        self._tilemap = [[None for _ in range(h)] for _ in range(w)]
        self._size = s

    def set_tile(self, x, y, tile):
        self._tilemap[x][y] = tile

    def get_tile(self, x, y):
        return self._tilemap[x][y]

    def on_draw(self):
        for x in range(len(self._tilemap)):
            for y in range(len(self._tilemap[x])):
                image = self._tilemap[x][y]
                if image is None:
                    continue

                w = self._size * self._concatenated_scale.x
                h = self._size * self._concatenated_scale.y
                lv = Vector2((x + 0.5) * w, (y + 0.5) * h)
                lr = radians(self._concatenated_rotation)
                if lr != 0:
                    lv = Vector2(lv.x * cos(lr) - lv.y * sin(lr), lv.x * sin(lr) + lv.y * cos(lr))

                v = camera.screen_position(self._concatenated_position + lv)
                s = camera.screen_size(Vector2(w, h))
                rad = radians(camera.screen_rotation(self._concatenated_rotation))

                if rad != 0:
                    image.rotate_draw(rad, floor(v.x), floor(v.y), ceil(s.x), ceil(s.y))
                else:
                    image.draw(floor(v.x), floor(v.y), ceil(s.x), ceil(s.y))
