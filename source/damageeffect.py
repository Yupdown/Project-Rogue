from worldobject import *


class DamageEffect(WorldObject):
    image = None

    def __init__(self, tile_map):
        super().__init__(tile_map)
        if DamageEffect.image is None:
            DamageEffect.image = get_image('txt_critical.png')
        self.renderer = PSpriteObject(DamageEffect.image)
        self.add_element(self.renderer)

    def update(self, delta_time):
        super().update(delta_time)
        factor = self.time * 3
        smooth_factor = 4 * factor ** 3 - 6 * factor ** 2 + 3 * factor
        self.renderer.set_position(Vector2(0, 20 + smooth_factor * 20) / PIXEL_PER_UNIT)
        self.renderer.set_scale(Vector2(1, 2 - smooth_factor * 2))
        if factor >= 1:
            self.get_parent().remove_world_object(self)