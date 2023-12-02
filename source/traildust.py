import random
from worldobject import *


class TrailDust(WorldObject):
    images = None

    def __init__(self, tile_map, velocity):
        super().__init__(tile_map)
        if TrailDust.images is None:
            TrailDust.images = [PSprite(get_image('effects.png'), i * 10, 118, 10, 10) for i in range(4)]
        self.rotation_velocity = random.randrange(-360, 360)
        self.velocity = velocity
        self.force = Vector2(0, 0)
        self.renderer = PSpriteObject(TrailDust.images[random.randrange(0, len(TrailDust.images))])
        self.add_element(self.renderer)

    def update(self, delta_time):
        super().update(delta_time)
        self.velocity = lerp(self.velocity, Vector2(0, 0), delta_time * 4)
        self.set_position(self.get_position() + self.velocity * delta_time)
        self.set_rotation(self.time * self.rotation_velocity)
        self.set_scale(Vector2(1, 1) * (1 - self.time))

        if self.time >= 1:
            self.get_parent().remove_world_object(self)