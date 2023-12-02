import random
from worldobject import *
from avatar import *
from traildust import *

class Player(WorldObject):
    def __init__(self, tile_map):
        super().__init__(tile_map)
        self.renderer = Avatar(get_image('werewolf01.png'))
        self.add_element(self.renderer)
        self.life = 6
        self.coins = 0
        self.wall_jump = 0
        self.coyote_jump = 0
        self.run_factor = 0
        self.animator = AvatarAnimator()
        self.direction = 1
        self.climb = 0
        self.emit_time = 0
        self.collision_tag = 'player'
        self.collision_bounds = (-0.1, 0, 0.1, 0.4)

        sobj_weapon = PSpriteObject(PSprite('weapons01.png', 89, 139, 17, 7))
        sobj_weapon.set_position(Vector2(-7 / PIXEL_PER_UNIT, 0))
        self.renderer.sobj_arm_bl.add_element(sobj_weapon)

    def update(self, delta_time):
        super().update(delta_time)

        self.emit_time -= delta_time
        self.update_movement(delta_time)

        if get_buttondown(SDL_BUTTON_LEFT):
            v = self.get_position()
            offset_x = self.direction * 0.4
            rect = (v.x + offset_x - 0.4, v.y, v.x + offset_x + 0.4, v.y + 0.4)
            for o in self.get_parent().get_collision_objects('monster', rect):
                print('affect ' + type(o).__name__)

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

        self.renderer.root.set_scale(Vector2(-self.direction, 1.0))
        self.animator.update(self, delta_time)

    def emit_trail_dust(self):
        dust_object = TrailDust(self.ref_tile_map, self.velocity * 0.25)
        dust_object.set_position(self.get_position() + Vector2(0, 0.1))
        self.get_parent().add_world_object(dust_object, 1)

    def update_movement(self, delta_time):
        self.wall_jump -= delta_time
        self.coyote_jump -= delta_time

        if not self.wall_jump > 0:
            flag = False
            if get_key(SDLK_a):
                self.force = Vector2(-100, self.force.y)
                self.direction = -1
                if self.collision & 4 and not self.collision & 2:
                    if self.velocity.y < 0:
                        self.velocity = Vector2(0, 0)
                    self.climb = 1
                    flag = True
            elif get_key(SDLK_d):
                self.force = Vector2(100, self.force.y)
                self.direction = 1
                if self.collision & 8 and not self.collision & 2:
                    if self.velocity.y < 0:
                        self.velocity = Vector2(0, 0)
                    self.climb = 2
                    flag = True
            else:
                self.force = Vector2(0, self.force.y)
            if flag:
                self.coyote_jump = 0.15
                if self.emit_time <= 0:
                    self.emit_trail_dust()
                    self.emit_time = 0.2
        else:
            if self.climb == 1:
                self.direction = -1
            elif self.climb == 2:
                self.direction = 1

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
