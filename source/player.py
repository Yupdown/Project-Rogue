import random
from worldobject import *
from avatar import *
from traildust import *
from slasheffect import *


class Player(WorldObject):
    def __init__(self, tile_map):
        super().__init__(tile_map)
        self.renderer = Avatar(get_image('werewolf01.png')) #
        self.add_element(self.renderer)
        self.life = 10
        self.coins = 0
        self.wall_jump = 0
        self.coyote_jump = 0
        self.run_factor = 0
        self.attack_factor = 0
        self.animator = AvatarAnimator()
        self.direction = 1
        self.climb = 0
        self.emit_time = 0
        self.attack_time = 0
        self.attack_type = 0
        self.evasion_time = 0
        self.collision_tag = 'player'
        self.collision_bounds = (-0.1, 0, 0.1, 0.4)
        self.walk_sound_type = 0
        self.damage_cool = 0

        sobj_weapon = PSpriteObject(PSprite('weapons01.png', 89, 139, 17, 7))
        sobj_weapon.set_position(Vector2(-7 / PIXEL_PER_UNIT, 0))
        self.renderer.sobj_arm_bl.add_element(sobj_weapon)

    def update(self, delta_time):
        super().update(delta_time)

        self.emit_time -= delta_time
        self.attack_time -= delta_time
        self.evasion_time -= delta_time
        self.damage_cool -= delta_time

        self.attack_factor = clamp(0, 1 - (self.attack_time / 0.4), 1)
        self.update_movement(delta_time)

        if get_keydown(SDLK_LSHIFT) and self.evasion_time <= 0 and self.collision & 2:
            self.velocity = Vector2(self.direction * 12, self.velocity.y)
            self.evasion_time = 0.5

            sfx = get_sound('jump2.wav')
            sfx.set_volume(100)
            sfx.play()

        if get_button(SDL_BUTTON_LEFT) and self.attack_time <= 0 and not self.wall_jump > 0 and not self.climb:
            slash_effect = SlashEffect(self.ref_tile_map)
            slash_effect.set_position(self.get_position())
            slash_effect.set_scale(Vector2(-self.direction, 1))
            self.get_parent().add_world_object(slash_effect)
            self.velocity += Vector2(self.direction * 3, 0)
            self.attack_time = 0.4
            self.attack_type = (self.attack_type + 1) % 2

            sfx = get_sound(['Swish2_1a.wav', 'Swish2_1c.wav'][self.attack_type])
            sfx.play()

            v = self.get_position()
            offset_x = self.direction * 0.5
            rect = (v.x + offset_x - 0.5, v.y, v.x + offset_x + 0.5, v.y + 0.5)

            hit_monsters = self.get_parent().get_collision_objects('monster', rect)
            if hit_monsters:
                self.get_parent().shake_camera()
                sfx = get_sound(['Bullet_Ground_1c.wav', 'Bullet_Ground_1d.wav'][self.attack_type])
                sfx.play()
            for hit_monster in hit_monsters:
                hit_monster.apply_damage(10, self)

        coins = self.get_parent().get_collision_objects_from_object('coin', self)
        got_coin = False
        for coin in coins:
            if coin.time < 0.25:
                continue
            got_coin = True
            self.coins += 1
            self.get_parent().remove_world_object(coin)
        if got_coin:
            sfx = get_sound('8BIT_RETRO_Coin_Collect_Two_Note_Twinkle_Fast_mono.wav')
            sfx.set_volume(15)
            sfx.play()

        if self.damage_cool <= 0 and self.evasion_time <= 0:
            monsters = self.get_parent().get_collision_objects_from_object('monster', self)
            projectiles = self.get_parent().get_collision_objects_from_object('projectile', self)
            if projectiles:
                self.damage()
                self.get_parent().remove_world_object(projectiles[0])
            elif monsters:
                self.damage()

        if self.attack_time <= -0.5:
            self.attack_type = 0

        if self.damage_cool > 0.75:
            self.animator.set_state(AnimationDamaged)
        elif self.evasion_time > 0:
            self.animator.set_state(AnimationJumpRoll)
        elif self.attack_time > 0:
            if self.attack_type == 0:
                self.animator.set_state(AnimationAttackUp)
            elif self.attack_type == 1:
                self.animator.set_state(AnimationAttackDown)
        elif self.collision & 2:
            if abs(self.velocity.x) > 0.1:
                self.animator.set_state(AnimationMove)
                if self.emit_time <= 0:
                    self.emit_trail_dust()
                    self.emit_time = 0.2
                    sfx = get_sound(['walk1.wav', 'walk2.wav'][self.walk_sound_type])
                    sfx.set_volume(50)
                    sfx.play()
                    self.walk_sound_type = (self.walk_sound_type + 1) % 2
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

    def damage(self):
        if self.damage_cool > 0 or self.evasion_time > 0:
            return
        self.get_parent().shake_camera(3)
        self.velocity = Vector2(8 * -self.direction, self.velocity.y)
        self.life -= 1
        self.damage_cool = 1
        get_sound('bonk.wav').play()
        if self.life <= 0:
            self.get_parent().notify_player_kill()
            self.get_parent().remove_world_object(self)

    def emit_trail_dust(self):
        dust_object = TrailDust(self.ref_tile_map, self.velocity * 0.25)
        dust_object.set_position(self.get_position() + Vector2(0, 0.1))
        self.get_parent().add_world_object(dust_object, 1)

    def update_movement(self, delta_time):
        self.wall_jump -= delta_time
        self.coyote_jump -= delta_time

        if not self.wall_jump > 0:
            flag = False
            self.force = Vector2(0, self.force.y)
            if not self.damage_cool > 0.75:
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
            if flag:
                self.coyote_jump = 0.15
                if self.emit_time <= 0:
                    self.emit_trail_dust()
                    self.emit_time = 0.2
        else:
            if self.climb == 1:
                self.direction = 1
            elif self.climb == 2:
                self.direction = -1

        if get_keydown(SDLK_SPACE):
            if self.coyote_jump > 0:
                self.coyote_jump = 0
                if self.climb > 0:
                    self.force = Vector2(100 if self.climb == 1 else -100, self.force.y)
                    self.velocity = Vector2(5 if self.climb == 1 else -5, 10)
                    self.wall_jump = 0.44
                    sfx = get_sound('jump2.wav')
                    sfx.set_volume(100)
                    sfx.play()
                else:
                    self.velocity = Vector2(self.velocity.x, 10)
                sfx = get_sound('jump1.wav')
                sfx.set_volume(50)
                sfx.play()

        self.update_physics(delta_time)
        self.run_factor += delta_time * self.velocity.x * 6

        if self.collision & 14:
            self.wall_jump = 0

        if self.collision & 2:
            self.climb = 0
            self.coyote_jump = 0.15
