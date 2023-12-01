import random

from worldobject import *
from avatar import *


class Monster(WorldObject):
    def __init__(self, tile_map):
        super().__init__(tile_map)
        self.behaviour = MonsterBehaviour()
        self.velocity_max = Vector2(2, 10)
        self.run_factor = 0

    def update(self, delta_time):
        self.behaviour.update(self, self.ref_tile_map)
        self.update_physics(delta_time)
        self.run_factor += delta_time * self.velocity.x * 6


class MonsterSlime(Monster):
    def __init__(self, tile_map):
        super().__init__(tile_map)

        image = get_image('slime%02d.png' % random.randint(1, 3))

        self.joint_face = PObject()
        self.joint_face.set_position(Vector2(0, 2) / PIXEL_PER_UNIT)

        self.sobj_eye_l = PSpriteObject(PSprite(image, 2, 0, 2, 2))
        self.sobj_eye_r = PSpriteObject(PSprite(image, 4, 0, 2, 2))
        self.sobj_mouth = PSpriteObject(PSprite(image, 6, 0, 2, 2))

        self.sobj_eye_l.set_position(Vector2(-2, 0) / PIXEL_PER_UNIT)
        self.sobj_eye_r.set_position(Vector2(2, 0) / PIXEL_PER_UNIT)
        self.sobj_mouth.set_position(Vector2(0, -1) / PIXEL_PER_UNIT)

        self.joint_face.add_element(self.sobj_eye_l)
        self.joint_face.add_element(self.sobj_eye_r)
        self.joint_face.add_element(self.sobj_mouth)

        self.sobj_body = PSpriteObject(PSprite(image, 0, 6, 16, 10))
        self.sobj_body.set_position(Vector2(0, 5) / PIXEL_PER_UNIT)

        self.renderer = PObject()
        self.renderer.add_element(self.sobj_body)
        self.renderer.add_element(self.joint_face)
        self.add_element(self.renderer)

    def update(self, delta_time):
        super().update(delta_time)
        self.renderer.set_scale(Vector2(-self.behaviour.direction, self.renderer.get_scale().y))


class MonsterGoblin(Monster):
    def __init__(self, tile_map):
        super().__init__(tile_map)
        self.renderer = Avatar(get_image('goblin%02d.png' % random.randint(1, 2)))
        self.add_element(self.renderer)
        self.animator = AvatarAnimator()
        self.animator.set_state(AnimationMove)

    def update(self, delta_time):
        super().update(delta_time)
        self.renderer.root.set_scale(Vector2(-self.behaviour.direction, self.renderer.root.get_scale().y))
        self.animator.update(self, delta_time)


class MonsterWizard(Monster):
    def __init__(self, tile_map):
        super().__init__(tile_map)
        self.renderer = Avatar(get_image('skelton%02d.png' % random.randint(1, 3)))
        self.add_element(self.renderer)
        self.animator = AvatarAnimator()
        self.animator.set_state(AnimationMove)

    def update(self, delta_time):
        super().update(delta_time)
        self.renderer.root.set_scale(Vector2(-self.behaviour.direction, self.renderer.root.get_scale().y))
        self.animator.update(self, delta_time)


class MonsterBehaviour:
    def __init__(self):
        self.direction = 1

    def update(self, owner: WorldObject, tilemap):

        if owner.collision & 2:
            owner_pos = owner.get_position()
            check_wall_pos = owner_pos + Vector2(0.5 * self.direction, 0)
            check_cliff_pos = owner_pos + Vector2(0.5 * self.direction, -0.5)

            tile1 = tilemap.get_tile(floor(check_wall_pos.x), floor(check_wall_pos.y))
            tile2 = tilemap.get_tile(floor(check_cliff_pos.x), floor(check_cliff_pos.y))

            if tile1 > 0 or not tile2 > 0:
                self.direction = -self.direction

        owner.force = Vector2(self.direction * 80, owner.force.y)
