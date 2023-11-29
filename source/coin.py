from picowork.pspriteobject import *
from picowork.psprite import *


class Coin(PObject):
    sprites = None

    def __init__(self, tile_map, player):
        super().__init__()
        if Coin.sprites is None:
            image = get_image('gold_s.png')
            Coin.sprites = [PSprite(image, i * 9, 0, 9, 8) for i in range(6)]
            self.ref_tile_map = tile_map

        self.velocity = Vector2()
        self.force = Vector2(0, -30)

        self.visual = PSpriteObject(Coin.sprites[0])
        self.visual.set_position(Vector2(0, 4) / PIXEL_PER_UNIT)
        self.add_element(self.visual)

        self.player = player
        self.time = 0

    def update(self, delta_time):
        self.time += delta_time

        self.velocity += self.force * delta_time

        pre_pos = self.get_position()
        post_pos = pre_pos + self.velocity * delta_time

        self.collision = self.ref_tile_map.apply_velocity(self, pre_pos, post_pos)
        self.visual.set_image(Coin.sprites[floor(self.time * 10 % 6)])