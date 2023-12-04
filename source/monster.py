import random
from picowork.pspriteuiobject import *
from worldobject import *
from avatar import *
from damageeffect import *
from coin import *
from fireball import *
from slasheffect import *


class Monster(WorldObject):
    def __init__(self, player, tile_map):
        super().__init__(tile_map)
        self.ref_player = player
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
        self.behaviour.update(self, self.ref_player, self.ref_tile_map, delta_time)
        self.update_physics(delta_time)
        self.run_factor += delta_time * self.velocity.x * 10

    def apply_damage(self, value, sender):
        self.life -= value
        self.velocity += Vector2(sender.direction * 8, 0)
        self.behaviour.damage()
        self.behaviour.direction = -sender.direction

        damage_effect = DamageEffect(self.ref_tile_map)
        damage_effect.set_position(self.get_position())
        self.get_parent().add_world_object(damage_effect)

        if self.life <= 0:
            self.kill()

    def kill(self):
        for _ in range(5):
            coin = Coin(self.ref_tile_map)
            coin.velocity = Vector2(random.random() * 2 - 1, random.random()) * 10
            coin.set_position(self.get_position())
            self.get_parent().add_world_object(coin)
        sfx = get_sound('worm-death-2.ogg')
        sfx.set_volume(100)
        sfx.play()
        self.get_parent().notify_monster_kill()
        self.get_parent().remove_world_object(self)


class MonsterSlime(Monster):
    def __init__(self, player, tile_map):
        super().__init__(player, tile_map)
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
    def __init__(self, player, tile_map):
        super().__init__(player, tile_map)
        self.behaviour = MonsterGoblinBehaviour()
        self.renderer = Avatar(get_image('goblin%02d.png' % random.randint(1, 2)))
        self.add_element(self.renderer)
        self.animator = AvatarAnimator()
        self.animator.set_state(AnimationMove)
        self.attack_factor = 0

        sobj_weapon = PSpriteObject(PSprite('weapons01.png', 144, 76, 17, 7))
        sobj_weapon.set_position(Vector2(-6 / PIXEL_PER_UNIT, 0))
        self.renderer.sobj_arm_bl.add_element(sobj_weapon)

    def update(self, delta_time):
        super().update(delta_time)

        self.attack_factor = clamp(0, 1 - (self.behaviour.attack_time % 0.5 / 0.5), 1)
        self.renderer.root.set_scale(Vector2(-self.behaviour.direction, self.renderer.root.get_scale().y))

        if self.behaviour.damage_time > 0:
            self.animator.set_state(AnimationDamaged)
        elif self.behaviour.attack_time > 1.5:
            self.animator.set_state(AnimationAttackUp)
        elif self.behaviour.attack_time > 1.0:
            self.animator.set_state(AnimationAttackDown)
        else:
            self.animator.set_state(AnimationMove)
        self.animator.update(self, delta_time)

    def melee_attack(self):
        v = self.get_position()
        offset_x = self.behaviour.direction * 0.5
        rect = (v.x + offset_x - 0.5, v.y, v.x + offset_x + 0.5, v.y + 0.5)
        player = self.get_parent().get_collision_objects('player', rect)
        if player:
            player[0].damage()

        slash_effect = SlashEffect(self.ref_tile_map)
        slash_effect.set_position(self.get_position())
        slash_effect.set_scale(Vector2(-self.behaviour.direction, 1))
        self.get_parent().add_world_object(slash_effect)


class MonsterWizard(Monster):
    def __init__(self, player, tile_map):
        super().__init__(player, tile_map)
        self.behaviour = MonsterWizardBehaviour()
        self.renderer = Avatar(get_image('skelton%02d.png' % random.randint(1, 3)))
        self.add_element(self.renderer)
        self.animator = AvatarAnimator()
        self.animator.set_state(AnimationMove)
        self.attack_factor = 0

        sobj_weapon = PSpriteObject(PSprite('weapons01.png', 108, 78, 17, 7))
        sobj_weapon.set_position(Vector2(-6 / PIXEL_PER_UNIT, 0))
        self.renderer.sobj_arm_bl.add_element(sobj_weapon)

    def update(self, delta_time):
        super().update(delta_time)

        self.attack_factor = clamp(0, 1 - ((self.behaviour.attack_time - 1.6) / 0.4), 1)
        self.renderer.root.set_scale(Vector2(-self.behaviour.direction, self.renderer.root.get_scale().y))

        if self.behaviour.damage_time > 0:
            self.animator.set_state(AnimationDamaged)
        elif self.attack_factor < 1:
            self.animator.set_state(AnimationAttackDown)
        else:
            self.animator.set_state(AnimationMove)
        self.animator.update(self, delta_time)

    def cast_fireball(self):
        instance = Fireball(self.ref_tile_map)
        instance.set_position(self.get_position() + Vector2(self.behaviour.direction * 0.25, 0.25))
        instance.force = Vector2(self.behaviour.direction * 4, 0)
        instance.velocity = instance.force
        self.get_parent().add_world_object(instance)

        slash_effect = SlashEffect(self.ref_tile_map)
        slash_effect.set_position(self.get_position())
        slash_effect.set_scale(Vector2(-self.behaviour.direction, 1))
        self.get_parent().add_world_object(slash_effect)


class MonsterBehaviour:
    def __init__(self):
        self.direction = 1
        self.damage_time = 0

    def update(self, owner, player, tilemap, delta_time):
        self.damage_time -= delta_time
        self.update_move(owner, tilemap, delta_time)

    def update_move(self, owner, tilemap, delta_time):
        if owner.collision & 2:
            owner_pos = owner.get_position()
            check_wall_pos = owner_pos + Vector2(0.25 * self.direction, 0)
            check_cliff_pos = owner_pos + Vector2(0.25 * self.direction, -0.5)

            tile1 = tilemap.get_tile(floor(check_wall_pos.x), floor(check_wall_pos.y))
            tile2 = tilemap.get_tile(floor(check_cliff_pos.x), floor(check_cliff_pos.y))

            if tile1 > 0 or not tile2 > 0:
                self.direction = -self.direction

        if self.move_interrupt():
            owner.force = Vector2(0, owner.force.y)
        else:
            owner.force = Vector2(self.direction * 80, owner.force.y)

    def damage(self):
        self.damage_time = 0.3

    def move_interrupt(self):
        return self.damage_time > 0


class MonsterGoblinBehaviour(MonsterBehaviour):
    def __init__(self):
        super().__init__()
        self.attack_time = 0

    def update(self, owner, player, tilemap, delta_time):
        if self.damage_time <= 0:
            last_time = self.attack_time
            self.attack_time -= delta_time
            if last_time > 1.5 and self.attack_time <= 1.5:
                owner.melee_attack()
            dv = player.get_position() - owner.get_position()
            if self.attack_time <= 0 and dv.magnitude() < 1 and dv.x * self.direction > 0:
                self.attack_time = 2
        super().update(owner, player, tilemap, delta_time)

    def move_interrupt(self):
        return super().move_interrupt() or self.attack_time > 0.5


class MonsterWizardBehaviour(MonsterBehaviour):
    def __init__(self):
        super().__init__()
        self.attack_time = 0

    def update(self, owner, player, tilemap, delta_time):
        if self.damage_time <= 0:
            self.attack_time -= delta_time
            if self.attack_time <= 0:
                owner.cast_fireball()
                self.attack_time = 2
        super().update(owner, player, tilemap, delta_time)

    def move_interrupt(self):
        return super().move_interrupt() or self.attack_time > 1.5


class InterfaceMonsterLife(PObject):
    def __init__(self, monster):
        super().__init__()
        self.ref_monster = monster
        self.sprite_back = get_image('life_frame_s.png')
        self.sprite_fill = get_image('life_value_s.png')

    def on_draw(self):
        factor = self.ref_monster.life / self.ref_monster.max_life
        if factor >= 1:
            return
        v = camera.world_to_screen(self._concatenated_position)
        w = self.sprite_back.w * self._concatenated_scale.x * UI_SCALE_MULTIPLY
        h = self.sprite_back.h * self._concatenated_scale.y * UI_SCALE_MULTIPLY
        self.sprite_back.draw(v.x, v.y, w, h)
        self.sprite_fill.clip_draw(0, 0, floor(self.sprite_fill.w * factor), self.sprite_fill.h, v.x - (w / 2 * (1 - factor)), v.y, w * factor, h)