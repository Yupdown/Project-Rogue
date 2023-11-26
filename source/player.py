import random

from picowork import picowork
from picowork.presource import *
from picowork.pspriteobject import *
from picowork.psprite import *
from picowork.pinput import *

class Player(PObject):
    def __init__(self, tile_map):
        super().__init__()
        self.renderer = PlayerRenderer(get_image('avatar_body0005.png'))
        self.add_element(self.renderer)
        self.velocity = Vector2()
        self.force = Vector2(0, -30)
        self.velocity_max = Vector2(5, 10)
        self.friction = 30
        self.ref_tile_map = tile_map
        self.collision = 0
        self.wall_jump = 0
        self.coyote_jump = 0
        self.run_factor = 0
        self.animator = CharacterAnimator()
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

        self.run_factor += delta_time * self.velocity.x * 6

        self.collision = self.ref_tile_map.apply_velocity(self, pre_pos, post_pos)
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


class PlayerRenderer(PObject):
    def __init__(self, image):
        super().__init__()
        self.root = PObject()

        self.joint_hips = PObject()
        self.joint_hip_l = PObject()
        self.joint_hip_r = PObject()
        self.joint_shoulder_l = PObject()
        self.joint_shoulder_r = PObject()

        self.sobj_head = PSpriteObject(PSprite(image, 0, 20, 16, 12))
        self.sobj_head_back = PSpriteObject(PSprite(image, 16, 20, 16, 12))
        self.sobj_body = PSpriteObject(PSprite(image, 0, 10, 10, 10))
        self.sobj_body_back = PSpriteObject(PSprite(image, 10, 10, 10, 10))
        self.sobj_eye_l = PSpriteObject(PSprite(image, 14, 0, 2, 2))
        self.sobj_eye_r = PSpriteObject(PSprite(image, 16, 0, 2, 2))

        self.sobj_arm_bl = PSpriteObject(PSprite(image, 22, 14, 2, 4))
        self.sobj_arm_br = PSpriteObject(PSprite(image, 26, 14, 2, 4))
        self.sobj_leg_bl = PSpriteObject(PSprite(image, 3, 0, 2, 4))
        self.sobj_leg_br = PSpriteObject(PSprite(image, 9, 0, 2, 4))

        self.joint_hips.set_position(Vector2(0.0, 3.5) / PIXEL_PER_UNIT)
        self.joint_hip_l.set_position(Vector2(-1, 0) / PIXEL_PER_UNIT)
        self.joint_hip_r.set_position(Vector2(2, 0) / PIXEL_PER_UNIT)
        self.joint_shoulder_l.set_position(Vector2(-1, 3.5) / PIXEL_PER_UNIT)
        self.joint_shoulder_r.set_position(Vector2(2, 3.5) / PIXEL_PER_UNIT)
        self.joint_shoulder_l.set_rotation(-15)
        self.joint_shoulder_r.set_rotation(15)

        self.sobj_body.set_position(Vector2(0, 2.5) / PIXEL_PER_UNIT)
        self.sobj_body_back.set_position(Vector2(0, -0.5) / PIXEL_PER_UNIT)
        self.sobj_head.set_position(Vector2(0, 8.5) / PIXEL_PER_UNIT)
        self.sobj_head_back.set_position(Vector2(4, -5) / PIXEL_PER_UNIT)

        self.sobj_arm_bl.set_position(Vector2(0, -4.5) / PIXEL_PER_UNIT)
        self.sobj_arm_br.set_position(Vector2(0, -4.5) / PIXEL_PER_UNIT)

        self.sobj_leg_bl.set_position(Vector2(0, -3) / PIXEL_PER_UNIT)
        self.sobj_leg_br.set_position(Vector2(0, -3) / PIXEL_PER_UNIT)

        self.sobj_eye_l.set_position(Vector2(-2, -2) / PIXEL_PER_UNIT)
        self.sobj_eye_r.set_position(Vector2(1, -2) / PIXEL_PER_UNIT)

        self.add_element(self.root)

        self.joint_hip_l.add_element(self.sobj_leg_bl)
        self.joint_hip_r.add_element(self.sobj_leg_br)

        self.joint_shoulder_l.add_element(self.sobj_arm_bl)
        self.joint_shoulder_r.add_element(self.sobj_arm_br)

        self.joint_hips.add_element(self.joint_hip_l)
        self.joint_hips.add_element(self.joint_hip_r)
        self.joint_hips.add_element(self.joint_shoulder_l)
        self.joint_hips.add_element(self.sobj_body_back)
        self.joint_hips.add_element(self.sobj_body)
        self.joint_hips.add_element(self.joint_shoulder_r)
        self.joint_hips.add_element(self.sobj_head)

        self.sobj_head.add_element(self.sobj_head_back)

        self.root.add_element(self.joint_hips)

        self.sobj_head.add_element(self.sobj_eye_l)
        self.sobj_head.add_element(self.sobj_eye_r)

class CharacterAnimator:
    def __init__(self):
        self.current_state = None

    def update(self, character: Player, delta_time):
        if self.current_state is not None:
            self.current_state.update(character, character.renderer, delta_time)

    def set_state(self, state):
        self.current_state = state


class AnimationIdle:
    @staticmethod
    def update(character, renderer, delta_time):
        renderer.root.set_rotation(0)
        renderer.joint_hips.set_rotation(0)
        renderer.joint_shoulder_l.set_rotation(-15)
        renderer.joint_shoulder_r.set_rotation(15)


class AnimationMove:
    @staticmethod
    def update(character, renderer, delta_time):
        renderer.root.set_rotation(-character.velocity.x * (sin(character.run_factor) + 1.5) * 2)
        renderer.joint_hips.set_rotation(0)
        renderer.joint_shoulder_l.set_rotation(-character.velocity.x * sin(character.run_factor / 2) * 15 - 15)
        renderer.joint_shoulder_r.set_rotation(-character.velocity.x * sin(character.run_factor / 2 + math.pi) * 15 + 15)
        renderer.joint_hip_l.set_rotation(-character.velocity.x * sin(character.run_factor / 2 + math.pi) * 10)
        renderer.joint_hip_r.set_rotation(-character.velocity.x * sin(character.run_factor / 2) * 10)

class AnimationJump:
    @staticmethod
    def update(character, renderer, delta_time):
        renderer.root.set_rotation(lerp(renderer.root.get_rotation(), 0, delta_time * 8))
        renderer.joint_hips.set_rotation(lerp(renderer.joint_hips.get_rotation(), 0, delta_time * 8))
        renderer.joint_hip_l.set_rotation(30)
        renderer.joint_hip_r.set_rotation(-30)
        pr = pow(character.velocity.y * 0.25, 3)
        renderer.joint_shoulder_l.set_rotation(pr * 10 - 90)
        renderer.joint_shoulder_r.set_rotation(pr * -10 + 90)


class AnimationJumpRoll:
    @staticmethod
    def update(character, renderer, delta_time):
            renderer.root.set_rotation(0)
            renderer.joint_hips.set_rotation(renderer.joint_hips.get_rotation() - 2000 * delta_time)

class AnimationClimb:
    @staticmethod
    def update(character, renderer, delta_time):
        renderer.joint_hips.set_rotation(0)
        if character.collision & 4:
            renderer.root.set_scale(Vector2(-1.0, 1.0))
            renderer.root.set_rotation(-30)
        elif character.collision & 8:
            renderer.root.set_scale(Vector2(1.0, 1.0))
            renderer.root.set_rotation(30)
        renderer.joint_shoulder_l.set_rotation(-30)
        renderer.joint_shoulder_r.set_rotation(90)