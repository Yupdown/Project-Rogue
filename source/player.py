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
        self.ref_tile_map = tile_map
        self.landed = False

    def update(self, delta_time):
        if get_key(SDLK_a):
            self.force = Vector2(-100, self.force.y)
            self.renderer.set_scale(Vector2(1.0, 1.0))
        elif get_key(SDLK_d):
            self.force = Vector2(100, self.force.y)
            self.renderer.set_scale(Vector2(-1.0, 1.0))
        else:
            self.force = Vector2(0, self.force.y)

        if get_keydown(SDLK_SPACE) and self.landed:
            self.velocity = Vector2(self.velocity.x, 30)

        self.velocity += self.force * delta_time
        self.velocity = Vector2(
            clamp(-self.velocity_max.x, self.velocity.x, self.velocity_max.x),
            clamp(-self.velocity_max.y, self.velocity.y, self.velocity_max.y))
        if self.velocity.x > 0:
            self.velocity = Vector2(max(self.velocity.x - 30 * delta_time, 0), self.velocity.y)
        else:
            self.velocity = Vector2(min(self.velocity.x + 30 * delta_time, 0), self.velocity.y)

        pre_pos = self.get_position()
        post_pos = pre_pos + self.velocity * delta_time

        self.landed = self.ref_tile_map.apply_velocity(self, pre_pos, post_pos)
        self.renderer.root.set_rotation(-self.velocity.x * 3)

class PlayerRenderer(PObject):
    def __init__(self, image):
        super().__init__()
        self.root = PObject()

        self.sobj_head = PSpriteObject(PSprite(image, 0, 20, 16, 12))
        self.sobj_head_back = PSpriteObject(PSprite(image, 16, 20, 16, 12))
        self.sobj_body = PSpriteObject(PSprite(image, 0, 10, 10, 10))
        self.sobj_body_back = PSpriteObject(PSprite(image, 10, 10, 10, 10))
        self.sobj_hips = PSpriteObject(PSprite(image, 20, 2, 8, 8))
        self.sobj_eye_l = PSpriteObject(PSprite(image, 14, 0, 2, 2))
        self.sobj_eye_r = PSpriteObject(PSprite(image, 16, 0, 2, 2))

        self.sobj_arm_bl = PSpriteObject(PSprite(image, 20, 15, 4, 5))
        self.sobj_arm_br = PSpriteObject(PSprite(image, 24, 15, 4, 5))
        self.sobj_leg_bl = PSpriteObject(PSprite(image, 0, 0, 6, 5))
        self.sobj_leg_br = PSpriteObject(PSprite(image, 6, 0, 6, 5))

        self.sobj_body.set_position(Vector2(0.02, 0.18))
        self.sobj_body_back.set_position(Vector2(0.02, 0.18))
        self.sobj_head.set_position(Vector2(0.015, 0.37))
        self.sobj_head_back.set_position(Vector2(0.1, 0.37))

        self.sobj_arm_bl.set_position(Vector2(-0.07, 0.125))
        self.sobj_arm_br.set_position(Vector2(0.08, 0.125))
        self.sobj_arm_bl.set_rotation(-10.0)
        self.sobj_arm_br.set_rotation(10.0)

        self.sobj_leg_bl.set_position(Vector2(-0.04, 0.045))
        self.sobj_leg_br.set_position(Vector2(0.05, 0.045))
        self.sobj_hips.set_position(Vector2(-0.01, 0.12))

        self.sobj_eye_l.set_position(Vector2(-0.05, 0.31))
        self.sobj_eye_r.set_position(Vector2(0.0425, 0.31))

        self.add_element(self.root)

        self.root.add_element(self.sobj_arm_bl)
        self.root.add_element(self.sobj_leg_bl)
        self.root.add_element(self.sobj_leg_br)

        self.root.add_element(self.sobj_body_back)
        self.root.add_element(self.sobj_body)
        self.root.add_element(self.sobj_hips)
        self.root.add_element(self.sobj_head_back)
        self.root.add_element(self.sobj_head)

        self.root.add_element(self.sobj_arm_br)
        self.root.add_element(self.sobj_eye_l)
        self.root.add_element(self.sobj_eye_r)