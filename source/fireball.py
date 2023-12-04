from worldobject import *
from picowork.psprite import *


class Fireball(WorldObject):
    sprites = None

    def __init__(self, tile_map):
        super().__init__(tile_map)

        self.collision_tag = 'projectile'
        self.collision_bounds = (-0.1, -0.1, 0.1, 0.1)

        if Fireball.sprites is None:
            image = get_image('effects.png')
            Fireball.sprites = [PSprite(image, i * 11, 110, 11, 7) for i in range(4)]

        self.visual = PSpriteObject(Fireball.sprites[0])
        self.add_element(self.visual)

    def update(self, delta_time):
        super().update(delta_time)
        post_pos = self.get_position() + self.velocity * delta_time
        self.collision = self.ref_tile_map.apply_velocity(self, self.get_position(), post_pos)
        self.set_rotation(degrees(atan2(self.velocity.y, self.velocity.x)) + 180)
        self.visual.set_image(Fireball.sprites[floor(self.time * 10 % 4)])
        if self.collision:
            self.get_parent().remove_world_object(self)