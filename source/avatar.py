from picowork.psprite import *
from picowork.pspriteobject import *

class Avatar(PObject):
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

        # self.sobj_head.add_element(self.sobj_head_back)

        self.root.add_element(self.joint_hips)

        self.sobj_head.add_element(self.sobj_eye_l)
        self.sobj_head.add_element(self.sobj_eye_r)


class AvatarAnimator:
    def __init__(self):
        self.current_state = None

    def update(self, character, delta_time):
        if self.current_state is not None:
            self.current_state.update(character, character.renderer, delta_time)

    def set_state(self, state):
        self.current_state = state


class AnimationIdle:
    @staticmethod
    def update(character, renderer, delta_time):
        idle_time = character.time * 4
        renderer.root.set_rotation(0)
        renderer.joint_hips.set_rotation(pow(cos(idle_time) * 0.5 + 0.5, 0.5) * 2)
        renderer.joint_shoulder_l.set_rotation(-(15 + sin(idle_time) * 5))
        renderer.joint_shoulder_r.set_rotation(15 + sin(idle_time) * 5)
        renderer.joint_hip_l.set_rotation(0)
        renderer.joint_hip_r.set_rotation(0)


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
        renderer.joint_hips.set_rotation(renderer.joint_hips.get_rotation() + 2000 * delta_time)


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


class AnimationAttackDown:
    @staticmethod
    def update(character, renderer, delta_time):
        factor = 1 - (1 - character.attack_factor) ** 10
        factor_shake = sin(character.time * 80) * (1 - character.attack_factor)
        renderer.root.set_rotation(0)
        renderer.joint_shoulder_l.set_rotation(180 + 180 * factor + factor_shake * 10)
        renderer.joint_shoulder_r.set_rotation(90 * factor + factor_shake * 20)
        renderer.joint_hip_l.set_rotation(-45 * factor)
        renderer.joint_hip_r.set_rotation(60 * factor)
        renderer.joint_hips.set_rotation(45 - (1 - factor) * 60)


class AnimationAttackUp:
    @staticmethod
    def update(character, renderer, delta_time):
        factor = 1 - (1 - character.attack_factor) ** 10
        factor_shake = sin(character.time * 80) * (1 - character.attack_factor)
        renderer.root.set_rotation(0)
        renderer.joint_shoulder_l.set_rotation(-factor * 180 + factor_shake * 10)
        renderer.joint_shoulder_r.set_rotation(90 * factor + factor_shake * 20)
        renderer.joint_hip_l.set_rotation(45 * factor)
        renderer.joint_hip_r.set_rotation(-60 * factor + 30)
        renderer.joint_hips.set_rotation(45 - factor * 90)


class AnimationDamaged:
    @staticmethod
    def update(character, renderer, delta_time):
        renderer.root.set_rotation(0)
        renderer.joint_hips.set_rotation(lerp( renderer.joint_hips.get_rotation(), -30, delta_time * 32))
        renderer.joint_shoulder_l.set_rotation(lerp(renderer.joint_shoulder_l.get_rotation(), -90, delta_time * 32))
        renderer.joint_shoulder_r.set_rotation(lerp(renderer.joint_shoulder_r.get_rotation(), -90, delta_time * 32))
