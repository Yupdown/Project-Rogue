from worldobject import *


class SlashEffect(WorldObject):
    image = None

    def __init__(self, tile_map):
        super().__init__(tile_map)
        if SlashEffect.image is None:
            SlashEffect.image = PSprite('effects.png', 60, 103, 15, 25)
        self.renderer = PSpriteObject(SlashEffect.image)
        self.renderer.set_position(Vector2(-12, 10) / PIXEL_PER_UNIT)
        self.add_element(self.renderer)

    def update(self, delta_time):
        super().update(delta_time)
        factor = self.time * 4
        self.renderer.set_position(Vector2(-(12 + pow(factor, 0.5) * 8), 10) / PIXEL_PER_UNIT)
        self.renderer.set_scale(Vector2(1 - pow(factor, 4), 1))
        if factor >= 1:
            self.get_parent().remove_world_object(self)