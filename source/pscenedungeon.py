from psceneworld import *
from picowork.pspriteobject import *
from picowork.pscrollpattern import *
from picowork.pspriteuiobject import *
from picowork.pfixedbackground import *
from picowork.ptextuiobject import *
from tilemapgeneration import *
from tilemap import *
from portal import *
import globalvariables


class PSceneDungeon(PSceneWorld):
    def __init__(self):
        super().__init__()

        self.rooms_visited = set()
        self.game_over = False

        self.camera_size = 4
        self.camera_shake = 0

        background_sky = PFixedBackground('skybox.png')
        self.add_element(background_sky)

        background = PScrollPattern('bg01_far.png', 20)
        background.set_position(Vector2(0, 40))
        self.add_element(background)

        background_near0 = PScrollPattern('bg01_mid.png', 15)
        background_near0.set_position(Vector2(0, 30))
        self.add_element(background_near0)

        background_near1 = PScrollPattern('bg01_mid.png', 12)
        background_near1.set_position(Vector2(0, 24))
        self.add_element(background_near1)

        background_near2 = PScrollPattern('bg01_mid.png', 10)
        background_near2.set_position(Vector2(0, 20))
        self.add_element(background_near2)

        self.tilemap = Tilemap(160, 100, 'terr02_%02d.png', ['fill03.png', 'fill02.png'])
        self.add_element(self.tilemap)

        portal_position = Vector2(18, 50)

        self.player = Player(self.tilemap)
        self.player.set_position(portal_position)
        self.add_world_object(self.player, 2)

        self.remain_monsters = 0
        self.current_room = None

        import scenemanagement
        self.portal = Portal(self.tilemap, self.player, scenemanagement.load_scene_village)
        self.portal.set_position(portal_position)
        self.add_world_object(self.portal)

        camera._position = self.player.get_position()

        self.interface = InterfaceDungeon(self.player)
        self.interface_gameover = InterfaceGameOver()
        self.add_element(self.interface, 5)

    def generate_dungeon(self):
        return generate_tilemap(self.tilemap, self.tilemap._w, self.tilemap._h, 13)

    def update(self, delta_time):
        super().update(delta_time)

        if get_keydown(SDLK_F12):
            globalvariables.DEBUG_MODE = not globalvariables.DEBUG_MODE
        if get_keydown(SDLK_END):
            import scenemanagement
            scenemanagement.load_scene_dungeon()
        if self.game_over and get_keydown(SDLK_SPACE):
            import scenemanagement
            scenemanagement.load_scene_village()

        new_campos = camera._position + (self.player.get_position() - camera._position) * delta_time * 8
        magnitude = clamp(-0.5, (new_campos - camera._position).x * 50, 0.5)

        v = self.player.get_position()
        r = self.tilemap.metadata['tile_to_room'][floor(v.x)][floor(v.y)]

        if r is not None and r not in self.rooms_visited:
            self.on_enter_new_room(r)
            self.rooms_visited.add(r)

        if self.current_room is not None:
            if globalvariables.DEBUG_MODE or self.remain_monsters <= 0:
                self.on_clear_new_room(self.current_room)

        self.camera_size = lerp(self.camera_size, 4 if r else 2.5, delta_time * 4)
        self.camera_shake = lerp(self.camera_shake, 0, delta_time * 3)

        camera._position = new_campos
        camera._rotation = magnitude
        camera._size = self.camera_size - self.camera_shake * 0.1

        self.interface.update(delta_time)
        if self.game_over:
            self.interface_gameover.update(delta_time)

    def on_generate_dungeon(self):
        pass

    def notify_monster_kill(self):
        self.remain_monsters -= 1

    def notify_player_kill(self):
        get_sound('UIImpact3.wav').play()
        self.shake_camera(3)
        self.game_over = True
        self.remove_element(self.interface)
        self.add_element(self.interface_gameover, 5)

    def shake_camera(self, value = 1):
        self.camera_shake = value

    def on_enter_new_room(self, room):
        if room.name == 'START ROOM':
            return
        self.current_room = room
        self.remain_monsters = 0
        if room.name == 'BOSS ROOM':
            bgm = get_music('music03.mp3')
            bgm.set_volume(50)
            bgm.repeat_play()
        for monster_type, x, y in self.tilemap.metadata['monsters'][room]:
            monster = monster_type(self.player, self.tilemap)
            monster.set_position(Vector2(x + 0.5, y))
            self.add_world_object(monster)
            for _ in range(8):
                dust_object = TrailDust(self.tilemap, Vector2(random.random() - 0.5, random.random() - 0.5) * 2)
                dust_object.set_position(monster.get_position() + Vector2(0, 0.1))
                self.add_world_object(dust_object, 1)
            self.remain_monsters += 1
        for facet_position in room.get_facet_positions():
            self.tilemap.set_tile(facet_position[0], facet_position[1], 1, False)
        get_sound('Drafted_1b.wav').play()

    def on_clear_new_room(self, room):
        self.current_room = None
        for facet in room.get_facet_positions():
            for _ in range(8):
                dust_object = TrailDust(self.tilemap, Vector2(random.random() - 0.5, random.random() - 0.5) * 4)
                dust_object.set_position(Vector2(facet[0] + 0.5, facet[1] + 0.5))
                self.add_world_object(dust_object, 1)
            self.tilemap.set_tile(facet[0], facet[1], -1, False)
        get_sound('DraftOff.wav').play()


class InterfaceDungeon(PObject):
    coin_sprites = None
    vignette_sprite = None

    def __init__(self, player):
        super().__init__()
        self.ref_player = player

        self.ui_coin_panel = PSpriteUIObject('pnl_have.png')
        self.ui_coin_panel.set_position(Vector2(get_canvas_width() - 110, get_canvas_height() - 30))
        self.add_element(self.ui_coin_panel)

        self.ui_coin_text = PTextUIObject('####', (226, 216, 211))
        self.ui_coin_text.set_position(Vector2(-5, 1))
        self.ui_coin_panel.add_element(self.ui_coin_text)

        if InterfaceDungeon.coin_sprites is None:
            image = get_image('gold_l.png')
            InterfaceDungeon.coin_sprites = [PSprite(image, i * 9, 0, 9, 14) for i in range(6)]
        if InterfaceDungeon.vignette_sprite is None:
            InterfaceDungeon.vignette_sprite = get_image('damage_vignette.png')

        self.ui_coin_icon = PSpriteUIObject(InterfaceDungeon.coin_sprites[0])
        self.ui_coin_icon.set_position(Vector2(-62.5, 0))
        self.ui_coin_icon.set_scale(Vector2(0.75, 0.75))
        self.ui_coin_panel.add_element(self.ui_coin_icon)
        self.last_coin = player.coins
        self.time = 0

        self.floating_coins = []

        self.ui_player_life = InterfacePlayerLife(player)
        self.ui_player_life.set_position(Vector2(0, get_canvas_height() - 4))
        self.add_element(self.ui_player_life)

    def update(self, delta_time):
        self.time += delta_time
        current_coin = self.ref_player.coins
        current_coin_image = InterfaceDungeon.coin_sprites[floor(self.time * 10 % 6)]
        for _ in range(current_coin - self.last_coin):
            floating_coin = (self.time, PSpriteUIObject(InterfaceDungeon.coin_sprites[0]))
            floating_coin[1].set_position(Vector2(get_canvas_width() / 2, get_canvas_height() / 2))
            floating_coin[1].set_scale(Vector2(0.25, 0.25))
            self.add_element(floating_coin[1])
            self.floating_coins.append(floating_coin)
        self.last_coin = current_coin
        self.ui_coin_text.set_text('%04d' % current_coin)
        self.ui_coin_icon.set_image(current_coin_image)

        for floating_coin in self.floating_coins:
            floating_coin[1].set_position(lerp(
                    floating_coin[1].get_position(),
                    self.ui_coin_panel.get_position() + self.ui_coin_icon.get_position(),
                    delta_time * 8))
            floating_coin[1].set_scale(lerp(
                    floating_coin[1].get_scale(),
                    self.ui_coin_icon.get_scale(),
                    delta_time * 8))
            floating_coin[1].set_image(current_coin_image)
            if self.time - floating_coin[0] >= 1:
                self.remove_element(floating_coin[1])
                self.floating_coins.remove(floating_coin)

    def on_draw(self):
        InterfaceDungeon.vignette_sprite.opacify(max(0, self.ref_player.damage_cool ** 15))
        InterfaceDungeon.vignette_sprite.draw_to_origin(0, 0, get_canvas_width(), get_canvas_height())


class InterfaceGameOver(PObject):
    panel_sprite = None
    def __init__(self):
        super().__init__()
        if InterfaceGameOver.panel_sprite is None:
            InterfaceGameOver.panel_sprite = get_image('splash_solid.png')
        self.time = 0
        self.ui_gameover_text = PSpriteUIObject('txt_death.png')
        self.ui_gameover_text.set_position(Vector2(get_canvas_width() / 2, get_canvas_height() / 2))
        self.add_element(self.ui_gameover_text)

        self.ui_coin_text = PTextUIObject('PRESS SPACE TO RESTART')
        self.ui_coin_text.set_position(Vector2(get_canvas_width() / 2 - 180, 60))
        self.add_element(self.ui_coin_text)

    def update(self, delta_time):
        self.time += delta_time
        factor = 1 - (clamp(0, self.time * 1.5, 1) - 1) ** 2
        self.ui_gameover_text.set_scale(Vector2(1, 1) * (sin(self.time * 4) * 0.1 + 2 * factor))
        self.ui_gameover_text.set_rotation(cos(self.time * 4) * 5)

    def on_draw(self):
        InterfaceGameOver.panel_sprite.opacify(min(0.4, self.time))
        InterfaceGameOver.panel_sprite.draw_to_origin(0, 0, get_canvas_width(), get_canvas_height())
        InterfaceGameOver.panel_sprite.opacify(1)

class InterfacePlayerLife(PObject):
    def __init__(self, player):
        super().__init__()
        self.ref_player = player
        self.sprite_back = get_image('life_frame.png')
        self.sprite_fill = get_image('life_value.png')

    def on_draw(self):
        v = Vector2(self._concatenated_position.x, self._concatenated_position.y)
        w = self.sprite_back.w * self._concatenated_scale.x * UI_SCALE_MULTIPLY
        h = self.sprite_back.h * self._concatenated_scale.y * UI_SCALE_MULTIPLY
        value = self.ref_player.life
        for index in range(5):
            factor = clamp(0, (value - index * 2) * 0.5, 1)
            factor = ceil(self.sprite_fill.w * factor) / self.sprite_fill.w
            self.sprite_back.draw_to_origin(v.x + index * 75, v.y - h, w, h)
            self.sprite_fill.clip_draw_to_origin(0, 0, ceil(self.sprite_fill.w * factor), self.sprite_fill.h, v.x + index * 75, v.y - h, w * factor, h)