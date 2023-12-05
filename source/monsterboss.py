import random
from picowork.pspriteuiobject import *
from worldobject import *
from avatar import *
from damageeffect import *
from coin import *
from fireball import *
from slasheffect import *


class MonsterBoss(WorldObject):
    def __init__(self, player, tile_map):
        super().__init__(tile_map)

        self.collision_tag = 'boss'
        self.collision_bounds = (-0.8, -0.8, 0.8, 1.2)

        self.renderer = AvatarBoss()
        self.add_element(self.renderer)

        self.pattern = [self.attack_spike, self.attack_fireball,  self.attack_lightning]
        self.pattern_timer = 5

        self.fireball_count = 0
        self.fireball_time = 0

        self.spikes = []
        self.lightnings = []

        self.max_life = 300
        self.life = self.max_life

        self.interface = BossInterface(self)
        self.add_element(self.interface)

    def on_add_element(self):
        for i in range(18):
            spike = BossSpike(self.ref_tile_map)
            spike.set_position(Vector2(131.5 + i, 43))
            self.get_parent().add_world_object(spike, 0)
            self.spikes.append(spike)

        for i in range(9):
            lightning = BossLightning(self.ref_tile_map)
            lightning.set_position(Vector2(132 + i * 2, 46))
            self.get_parent().add_world_object(lightning, 0)
            self.lightnings.append(lightning)

    def update(self, delta_time):
        super().update(delta_time)

        self.pattern_timer -= delta_time
        if self.pattern_timer <= 0:
            current_pattern = self.pattern.pop(0)
            current_pattern()
            self.pattern.append(current_pattern)
            self.pattern_timer = 4

        if self.fireball_count > 0:
            self.fireball_time -= delta_time
            while self.fireball_time <= 0 and self.fireball_count > 0:
                rad = self.fireball_count
                instance = Fireball(self.ref_tile_map)
                instance.set_position(self.get_position())
                instance.force = Vector2(cos(rad), sin(rad)) * 3
                instance.velocity = instance.force
                self.get_parent().add_world_object(instance)
                self.fireball_count -= 1
                self.fireball_time += 0.02
                sfx = get_sound('Swish2_1a.wav')
                sfx.set_volume(50)
                sfx.play()
        else:
            self.fireball_time = 0

        t = self.time * 4
        self.renderer.joint_0.set_position(Vector2(0, sin(t + 2) / PIXEL_PER_UNIT))
        self.renderer.joint_1.set_position(Vector2(0, sin(t + 1) / PIXEL_PER_UNIT))
        self.renderer.joint_2.set_position(Vector2(0, sin(t + 0) / PIXEL_PER_UNIT * 4))

    def attack_spike(self):
        for i in range(len(self.spikes)):
            self.spikes[i].action_timer = i * 0.075 + 1

    def attack_fireball(self):
        self.fireball_count = 100

    def attack_lightning(self):
        for i in range(len(self.lightnings)):
            self.lightnings[i].action_timer = 3 - i * 0.15

    def apply_damage(self, value, sender):
        self.life -= value
        if self.life <= 0:
            self.kill()

    def kill(self):
        for _ in range(20):
            coin = Coin(self.ref_tile_map)
            coin.velocity = Vector2(random.random() * 2 - 1, random.random()) * 10
            coin.set_position(self.get_position())
            self.get_parent().add_world_object(coin, 1)
        self.get_parent().notify_monster_kill()
        self.get_parent().remove_world_object(self)


class AvatarBoss(PObject):
    def __init__(self):
        super().__init__()
        image = get_image('lich01.png')

        self.root = PObject()

        self.joint_0 = PObject()
        self.joint_1 = PObject()
        self.joint_2 = PObject()

        self.sobj_hood_back = PSpriteObject(PSprite(image, 55, 0, 56, 86))
        self.sobj_hood_front = PSpriteObject(PSprite(image, 0, 0, 56, 86))

        self.sobj_body = PSpriteObject(PSprite(image, 16, 86, 24, 42))
        self.sobj_head = PSpriteObject(PSprite(image, 0, 110, 16, 18))
        self.sobj_jaw = PSpriteObject(PSprite(image, 0, 100, 16, 10))

        self.sobj_hand_l = PSpriteObject(PSprite(image, 41, 112, 16, 16))
        self.sobj_hand_r = PSpriteObject(PSprite(image, 57, 112, 16, 16))

        self.sobj_body.set_position(Vector2(0, 10) / PIXEL_PER_UNIT)
        self.sobj_head.set_position(Vector2(-4, 32) / PIXEL_PER_UNIT)
        self.sobj_jaw.set_position(Vector2(-2, 25) / PIXEL_PER_UNIT)

        self.sobj_hand_l.set_position(Vector2(-30, -8) / PIXEL_PER_UNIT)
        self.sobj_hand_r.set_position(Vector2(20, -8) / PIXEL_PER_UNIT)

        self.joint_0.add_element(self.sobj_hood_back)
        self.joint_0.add_element(self.sobj_body)
        self.joint_1.add_element(self.sobj_jaw)
        self.joint_1.add_element(self.sobj_head)
        self.joint_1.add_element(self.sobj_hood_front)
        self.joint_2.add_element(self.sobj_hand_l)
        self.joint_2.add_element(self.sobj_hand_r)

        self.root.add_element(self.joint_0)
        self.root.add_element(self.joint_1)
        self.root.add_element(self.joint_2)

        self.add_element(self.root)


class BossSpike(WorldObject):
    def __init__(self, tile_map):
        super().__init__(tile_map)
        self.collision_tag = 'projectile_fixed'
        self.collision_bounds = (-0.5, 0, 0.5, 1)

        self.renderer = PSpriteObject('stone09c.png')
        self.add_element(self.renderer)
        self.action_timer = -10
        
    def update(self, delta_time):
        super().update(delta_time)
        last_timer = self.action_timer
        self.action_timer -= delta_time

        if last_timer > 0 and self.action_timer <= 0:
            sfx = get_sound('Stone_Drop_1a.wav')
            sfx.set_volume(50)
            sfx.play()
            player = self.get_parent().get_collision_objects_from_object('player', self)
            if player:
                player[0].damage()

        t = self.action_timer * 20
        self.renderer.set_position(Vector2(0, abs(cos(t) / (abs(t) + 1)) - 0.6))


class BossLightning(WorldObject):
    def __init__(self, tile_map):
        super().__init__(tile_map)
        self.collision_tag = 'projectile_fixed'
        self.collision_bounds = (-0.2, -3, 0.2, 7)
        self.renderer = PSpriteObject('lightning1.png')
        self.renderer.set_rotation(90)
        self.renderer.set_scale(Vector2(1, 0))
        self.add_element(self.renderer)
        self.action_timer = -10

    def update(self, delta_time):
        super().update(delta_time)
        last_timer = self.action_timer
        self.action_timer -= delta_time

        if last_timer > 0 and self.action_timer <= 0:
            sfx = get_sound('ShotChargeRifle_1a.wav')
            sfx.set_volume(50)
            sfx.play()
            player = self.get_parent().get_collision_objects_from_object('player', self)
            if player:
                player[0].damage()

        if abs(self.action_timer) < 1:
            t = self.action_timer * 20
            self.renderer.set_scale(Vector2(1, abs(cos(t) / (abs(t * 4) + 1))))
        else:
            self.renderer.set_scale(Vector2(1, 0))


class BossInterface(PObject):
    def __init__(self, boss):
        super().__init__()
        self.ref_boss = boss
        self.sprite_back = get_image('pnl_boss.png')
        self.sprite_front = get_image('boss_gauge.png')

    def on_draw(self):
        w = self.sprite_back.w * UI_SCALE_MULTIPLY
        h = self.sprite_back.h * UI_SCALE_MULTIPLY
        value = self.ref_boss.life / self.ref_boss.max_life
        self.sprite_back.draw(get_canvas_width() / 2, 40, w, h)
        self.sprite_front.draw_to_origin(
            get_canvas_width() / 2 - 6 * UI_SCALE_MULTIPLY,
            40 - 5 * UI_SCALE_MULTIPLY,
            value * 27 * UI_SCALE_MULTIPLY,
            10 * UI_SCALE_MULTIPLY)