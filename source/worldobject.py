from picowork.pspriteobject import *
from picowork.psprite import *
from picowork.pinput import *


class WorldObject(PObject):
    font = None
    def __init__(self, tile_map):
        super().__init__()
        self.velocity = Vector2()
        self.velocity_max = Vector2(5, 10)
        self.friction = 30
        self.force = Vector2(0, -30)
        self.ref_tile_map = tile_map
        self.collision = 0
        self.time = 0
        self.collision_tag = 'Default'
        self.collision_bounds = None

    def update(self, delta_time):
        self.time += delta_time

    def on_draw(self):
        if WorldObject.font is None:
            WorldObject.font = load_font('DungGeunMo.ttf', 16)
        if True or self.collision_bounds is None:
            return
        v = camera.world_to_screen(self._concatenated_position)
        l = camera.screen_size(self.collision_bounds[0] * self._concatenated_scale.x)
        b = camera.screen_size(self.collision_bounds[1] * self._concatenated_scale.y)
        r = camera.screen_size(self.collision_bounds[2] * self._concatenated_scale.x)
        t = camera.screen_size(self.collision_bounds[3] * self._concatenated_scale.y)
        draw_rectangle(v.x + l, v.y + b, v.x + r, v.y + t)
        WorldObject.font.draw(v.x + r + 4, v.y + 6, self.collision_tag, (255, 0, 0))

    def update_physics(self, delta_time):
        self.velocity += self.force * delta_time
        vm = self.velocity_max
        self.velocity = Vector2(
            clamp(-vm.x, self.velocity.x, vm.x),
            clamp(-vm.y, self.velocity.y, vm.y))

        f = self.friction if self.collision & 2 else self.friction * 0.5
        if self.velocity.x > 0:
            self.velocity = Vector2(max(self.velocity.x - f * delta_time, 0), self.velocity.y)
        else:
            self.velocity = Vector2(min(self.velocity.x + f * delta_time, 0), self.velocity.y)

        pre_pos = self.get_position()
        post_pos = pre_pos + self.velocity * delta_time

        self.collision = self.ref_tile_map.apply_velocity(self, pre_pos, post_pos)