import random
from worldobject import *
from avatar import *

class Player(WorldObject):
    def __init__(self, tile_map):
        super().__init__(tile_map)
        self.renderer = Avatar(get_image('avatar_body0005.png'))
        self.add_element(self.renderer)
        self.wall_jump = 0
        self.coyote_jump = 0
        self.run_factor = 0
        self.animator = AvatarAnimator()
        self.climb = 0
        self.emit_time = 0
        self.trail_dusts = []

    def update(self, delta_time):
        self.emit_time -= delta_time
        self.update_movement(delta_time)

        if self.collision & 2:
            if abs(self.velocity.x) > 0.1:
                self.animator.set_state(AnimationMove)
                if self.emit_time <= 0:
                    self.emit_trail_dust()
                    self.emit_time = 0.2
            else:
                self.animator.set_state(AnimationIdle)
        elif self.collision & 12:
            self.animator.set_state(AnimationClimb)
        else:
            if self.wall_jump > 0:
                self.animator.set_state(AnimationJumpRoll)
            else:
                self.animator.set_state(AnimationJump)
        self.animator.update(self, delta_time)

        for trail_dust in self.trail_dusts:
            if not trail_dust.update(delta_time):
                self.trail_dusts.remove(trail_dust)
                trail_dust.remove_from_parent()

    def emit_trail_dust(self):
        dust_object = TrailDust(self.velocity * 0.25)
        dust_object.set_position(self.get_position() + Vector2(0, 0.1))
        self.get_parent().add_element(dust_object, 1)
        self.trail_dusts.append(dust_object)

    def update_movement(self, delta_time):
        self.wall_jump -= delta_time
        self.coyote_jump -= delta_time

        if not self.wall_jump > 0:
            if get_key(SDLK_a):
                self.force = Vector2(-100, self.force.y)
                self.renderer.root.set_scale(Vector2(1.0, 1.0))
                if self.collision & 4 and not self.collision & 2:
                    if self.velocity.y < 0:
                        self.velocity = Vector2(0, 0)
                    self.climb = 1
                    self.coyote_jump = 0.15
            elif get_key(SDLK_d):
                self.force = Vector2(100, self.force.y)
                self.renderer.root.set_scale(Vector2(-1.0, 1.0))
                if self.collision & 8 and not self.collision & 2:
                    if self.velocity.y < 0:
                        self.velocity = Vector2(0, 0)
                    self.climb = 2
                    self.coyote_jump = 0.15
            else:
                self.force = Vector2(0, self.force.y)
        else:
            if self.climb == 1:
                self.renderer.root.set_scale(Vector2(1.0, 1.0))
            elif self.climb == 2:
                self.renderer.root.set_scale(Vector2(-1.0, 1.0))

        if get_keydown(SDLK_SPACE):
            if self.coyote_jump > 0:
                if self.climb > 0:
                    self.force = Vector2(30 if self.climb == 1 else -30, self.force.y)
                    self.velocity = Vector2(30 if self.climb == 1 else -30, 30)
                    self.wall_jump = 0.44
                else:
                    self.velocity = Vector2(self.velocity.x, 30)

        self.update_physics(delta_time)
        self.run_factor += delta_time * self.velocity.x * 6

        if self.collision & 14:
            self.wall_jump = 0

        if self.collision & 2:
            self.climb = 0
            self.coyote_jump = 0.15


class TrailDust(PSpriteObject):
    images = None

    def __init__(self, velocity):
        if TrailDust.images is None:
            TrailDust.images = [PSprite(get_image('effects.png'), i * 10, 118, 10, 10) for i in range(4)]
        super().__init__(TrailDust.images[random.randrange(0, len(TrailDust.images))])
        self.time = 0
        self.rotation_velocity = random.randrange(-360, 360)
        self.velocity = velocity

    def update(self, delta_time):
        self.time += delta_time
        self.velocity = lerp(self.velocity, Vector2(0, 0), delta_time * 4)
        self.set_scale(Vector2(1, 1) * (1 - self.time))
        self.set_rotation(self.time * self.rotation_velocity)
        self.set_position(self.get_position() + self.velocity * delta_time)
        if self.time >= 1:
            return False
        return True
