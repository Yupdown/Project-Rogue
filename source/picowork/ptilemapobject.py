from .pobject import *
from .pcamera import *
from .presource import *


class PTileMapObject(PObject):
    def __init__(self, w, h, s):
        super().__init__()
        self._w = w
        self._h = h
        self._tilemap = [[None for _ in range(h)] for _ in range(w)]
        self._size = s

    def set_tile(self, x, y, tile):
        self._tilemap[x][y] = tile

    def get_tile(self, x, y):
        return self._tilemap[x][y]

    def on_draw(self):
        w = self._size * self._concatenated_scale.x
        h = self._size * self._concatenated_scale.y
        s = camera.screen_size(Vector2(w, h))
        lr = radians(self._concatenated_rotation)

        bl = camera.screen_to_world(Vector2(0, 0))
        tr = camera.screen_to_world(Vector2(get_canvas_width(), get_canvas_height()))

        xmin = max(0, floor((bl.x - self._concatenated_position.x) / w))
        xmax = min(self._w, ceil((tr.x - self._concatenated_position.x) / w))
        ymin = max(0, floor((bl.y - self._concatenated_position.y) / h))
        ymax = min(self._h, ceil((tr.y - self._concatenated_position.y) / h))

        for x in range(xmin, xmax):
            for y in range(ymin, ymax):
                image = self._tilemap[x][y]
                if image is None:
                    continue

                lv = Vector2((x + 0.5) * w, (y + 0.5) * h)
                if lr != 0:
                    lv = Vector2(lv.x * cos(lr) - lv.y * sin(lr), lv.x * sin(lr) + lv.y * cos(lr))

                v = camera.world_to_screen(self._concatenated_position + lv)
                rad = radians(camera.screen_rotation(self._concatenated_rotation))

                if rad != 0:
                    image.rotate_draw(rad, floor(v.x), floor(v.y), ceil(s.x), ceil(s.y))
                else:
                    image.draw(floor(v.x), floor(v.y), ceil(s.x), ceil(s.y))
