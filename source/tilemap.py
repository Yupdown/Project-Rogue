import random

from picowork import picowork
from picowork.ptilemapobject import *
from picowork.presource import *

class Tilemap(PObject):
    def __init__(self, w, h, front_format, back_format):
        super().__init__()
        self._w = w
        self._h = h
        self._tilemap = [[random.randint(0, 1) for _ in range(h)] for _ in range(w)]
        self._image_front = [get_image(front_format % n) if n > 0 else None for n in range(0, 17)]
        self._image_back = get_image(back_format)
        self._tilemap_back = PTileMapObject(w, h, 32 / PIXEL_PER_UNIT)
        self._tilemap_front = PTileMapObject(w * 2 + 1, h * 2 + 1, 16 / PIXEL_PER_UNIT)
        self._tilemap_front.set_position(Vector2(-0.25, -0.25))
        self.add_element(self._tilemap_back)
        self.add_element(self._tilemap_front)

        for x in range(self._w):
            for y in range(self._h):
                self.update_tile(x, y)

    def set_tile(self, x, y, tile):
        self._tilemap[x][y] = tile

    def get_tile(self, x, y):
        return self._tilemap[x][y]

    def update_tile(self, x, y):
        solid = [[False for _ in range(2)] for _ in range(2)]
        image_grid = [[0 for _ in range(2)] for _ in range(2)]

        for dx in range(0, min(2, self._w - x)):
            for dy in range(0, min(2, self._h - y)):
                solid[dx][dy] = self._tilemap[x + dx][y + dy] > 0

        self._tilemap_back.set_tile(x, y, self._image_back if solid[0][0] else None)

        if solid[0][0] and not solid[0][1]:
            image_grid[0][1] = 2
        if not solid[0][0] and solid[0][1]:
            image_grid[0][1] = 10
        if solid[0][0] and not solid[1][0]:
            image_grid[1][0] = 8
        if not solid[0][0] and solid[1][0]:
            image_grid[1][0] = 7
        if solid[0][0]:
            if solid[1][1]:
                if not solid[0][1]:
                    image_grid[1][1] = 14
                if not solid[1][0]:
                    image_grid[1][1] = 15
            else:
                if solid[0][1] and solid[1][0]:
                    image_grid[1][1] = 13
                elif solid[0][1]:
                    image_grid[1][1] = 8
                elif solid[1][0]:
                    image_grid[1][1] = 2
                else:
                    image_grid[1][1] = 4
        else:
            if not solid[1][1]:
                if solid[0][1]:
                    image_grid[1][1] = 12
                if solid[1][0]:
                    image_grid[1][1] = 1
            else:
                if solid[0][1] and solid[1][0]:
                    image_grid[1][1] = 16
                elif solid[0][1]:
                    image_grid[1][1] = 10
                elif solid[1][0]:
                    image_grid[1][1] = 7
                else:
                    image_grid[1][1] = 9

        for dx in range(2):
            for dy in range(2):
                self._tilemap_front.set_tile(x * 2 + dx + 1, y * 2 + dy + 1, self._image_front[image_grid[dx][dy]])