import random
from picowork.pspriteuiobject import *
from worldobject import *
from avatar import *


class Monster(WorldObject):
    def __init__(self, tile_map):
        super().__init__(tile_map)
        self.behaviour = MonsterBehaviour()
        self.velocity_max = Vector2(2, 10)
        self.run_factor = 0
        self.max_life = 50
        self.life = self.max_life
        self.collision_tag = 'monster'
        self.collision_bounds = (-0.1, 0, 0.1, 0.4)
        self.ui_life = InterfaceMonsterLife(self)
        self.ui_life.set_position(Vector2(0, 0.65))
        self.add_element(self.ui_life)

    def update(self, delta_time):
        super().update(delta_time)
        self.behaviour.update(self, self.ref_tile_map)
        self.update_physics(delta_time)
        self.run_factor += delta_time * self.velocity.x * 10


class MonsterSlime(Monster):
    def __init__(self, tile_map):
        super().__init__(tile_map)
        self.collision_bounds = (-0.15, 0, 0.15, 0.2)

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
        self.renderer.set_scale(Vector2(-self.behaviour.direction, 1 - sin(self.run_factor) * 0.2))
        self.joint_face.set_position(Vector2(0, 2 + cos(self.run_factor)) / PIXEL_PER_UNIT)


class MonsterGoblin(Monster):
    def __init__(self, tile_map):
        super().__init__(tile_map)
        self.renderer = Avatar(get_image('goblin%02d.png' % random.randint(1, 2)))
        self.add_element(self.renderer)
        self.animator = AvatarAnimator()
        self.animator.set_state(AnimationMove)

        sobj_weapon = PSpriteObject(PSprite('weapons01.png', 144, 76, 17, 7))
        sobj_weapon.set_position(Vector2(-6 / PIXEL_PER_UNIT, 0))
        self.renderer.sobj_arm_bl.add_element(sobj_weapon)

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

        sobj_weapon = PSpriteObject(PSprite('weapons01.png', 108, 78, 17, 7))
        sobj_weapon.set_position(Vector2(-6 / PIXEL_PER_UNIT, 0))
        self.renderer.sobj_arm_bl.add_element(sobj_weapon)

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
            check_wall_pos = owner_pos + Vector2(0.25 * self.direction, 0)
            check_cliff_pos = owner_pos + Vector2(0.25 * self.direction, -0.5)

            tile1 = tilemap.get_tile(floor(check_wall_pos.x), floor(check_wall_pos.y))
            tile2 = tilemap.get_tile(floor(check_cliff_pos.x), floor(check_cliff_pos.y))

            if tile1 > 0 or not tile2 > 0:
                self.direction = -self.direction

        owner.force = Vector2(self.direction * 80, owner.force.y)


class InterfaceMonsterLife(PObject):
    def __init__(self, monster):
        super().__init__()
        self.ref_monster = monster
        self.sprite_back = get_image('life_frame_s.png')
        self.sprite_fill = get_image('life_value_s.png')

    def on_draw(self):
        v = camera.world_to_screen(self._concatenated_position)
        w = self.sprite_back.w * self._concatenated_scale.x * UI_SCALE_MULTIPLY
        h = self.sprite_back.h * self._concatenated_scale.y * UI_SCALE_MULTIPLY
        factor = self.ref_monster.life / self.ref_monster.max_life
        self.sprite_back.draw(v.x, v.y, w, h)
        self.sprite_fill.clip_draw(0, 0, floor(self.sprite_fill.w * factor), self.sprite_fill.h, v.x - (w / 2 * (1 - factor)), v.y, w * factor, h)