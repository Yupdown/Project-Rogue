from psceneworld import *
from picowork.pspriteobject import *
from picowork.pscrollpattern import *
from picowork.pspriteuiobject import *
from picowork.pfixedbackground import *
from picowork.ptextuiobject import *
from tilemapgeneration import *
from tilemap import *
from portal import *


class PSceneDungeon(PSceneWorld):
    def __init__(self):
        super().__init__()

        self.rooms_visited = set()

        background_sky = PFixedBackground('skybox.png')
        self.add_element(background_sky)

        background = PScrollPattern('bg01_far.png', 20)
        background.set_position(Vector2(0, 20))
        self.add_element(background)

        background_near0 = PScrollPattern('bg01_mid.png', 18)
        background_near0.set_position(Vector2(0, 12))
        self.add_element(background_near0)

        background_near1 = PScrollPattern('bg01_mid.png', 13)
        background_near1.set_position(Vector2(0, 11))
        self.add_element(background_near1)

        background_near2 = PScrollPattern('bg01_mid.png', 10)
        background_near2.set_position(Vector2(0, 10))
        self.add_element(background_near2)

        self.tilemap = Tilemap(160, 100, 'terr02_%02d.png', ['fill03.png', 'fill02.png'])
        self.add_element(self.tilemap)

        self.player = Player(self.tilemap)
        self.player.set_position(Vector2(18.5, 45))
        self.add_world_object(self.player, 2)

        import scenemanagement
        self.portal = Portal(self.tilemap, self.player, scenemanagement.load_scene_village)
        self.portal.set_position(Vector2(18.5, 45))
        self.add_world_object(self.portal)

        camera._position = self.player.get_position()

        self.interface = InterfaceDungeon(self.player)
        self.add_element(self.interface)

    def generate_dungeon(self):
        return generate_tilemap(self.tilemap, self.tilemap._w, self.tilemap._h, 13)

    def update(self, delta_time):
        super().update(delta_time)

        new_campos = camera._position + (self.player.get_position() - camera._position) * delta_time * 8
        magnitude = clamp(-0.5, (new_campos - camera._position).x * 50, 0.5)

        v = self.player.get_position()
        r = self.tilemap.metadata['tile_to_room'][floor(v.x)][floor(v.y)]

        if r not in self.rooms_visited:
            for monster_type, x, y in self.tilemap.metadata['monsters'][r]:
                monster = monster_type(self.tilemap)
                monster.set_position(Vector2(x + 0.5, y))
                self.add_world_object(monster)
                for _ in range(8):
                    dust_object = TrailDust(self.tilemap, Vector2(random.random() - 0.5, random.random() - 0.5) * 2)
                    dust_object.set_position(monster.get_position() + Vector2(0, 0.1))
                    self.add_world_object(dust_object, 1)
            self.rooms_visited.add(r)

        camera._position = new_campos
        camera._rotation = magnitude
        camera._size = lerp(camera._size, 4 if r else 2.5, delta_time * 4)

        self.interface.update(delta_time)

    def on_generate_dungeon(self):
        pass


class InterfaceDungeon(PObject):
    coin_sprites = None

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
        self.ui_coin_icon = PSpriteUIObject(InterfaceDungeon.coin_sprites[0])
        self.ui_coin_icon.set_position(Vector2(-62.5, 0))
        self.ui_coin_icon.set_scale(Vector2(0.75, 0.75))
        self.ui_coin_panel.add_element(self.ui_coin_icon)
        self.time = 0

        self.ui_player_life = InterfacePlayerLife(player)
        self.ui_player_life.set_position(Vector2(0, get_canvas_height() - 4))
        self.add_element(self.ui_player_life)

    def update(self, delta_time):
        self.time += delta_time
        self.ui_coin_text.set_text('%04d' % self.ref_player.coins)
        self.ui_coin_icon.set_image(InterfaceDungeon.coin_sprites[floor(self.time * 10 % 6)])


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
        for index in range(3):
            factor = clamp(0, (value - index * 2) * 0.5, 1)
            self.sprite_back.draw_to_origin(v.x + index * 75, v.y - h, w, h)
            self.sprite_fill.clip_draw_to_origin(0, 0, floor(self.sprite_fill.w * factor), self.sprite_fill.h, v.x + index * 75, v.y - h, w * factor, h)