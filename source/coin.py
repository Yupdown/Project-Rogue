from worldobject import *
from picowork.psprite import *


class Coin(WorldObject):
    sprites = None

    def __init__(self, tile_map, player):
        super().__init__(tile_map)
        if Coin.sprites is None:
            image = get_image('gold_s.png')
            Coin.sprites = [PSprite(image, i * 9, 0, 9, 8) for i in range(6)]

        self.visual = PSpriteObject(Coin.sprites[0])
        self.visual.set_position(Vector2(0, 4) / PIXEL_PER_UNIT)
        self.add_element(self.visual)

        self.player = player

    def update(self, delta_time):
        super().update(delta_time)
        self.update_physics(delta_time)
        self.visual.set_image(Coin.sprites[floor(self.time * 10 % 6)])