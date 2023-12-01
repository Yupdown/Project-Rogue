from picowork.pscene import *
from picowork.pspriteobject import *
from picowork.pscrollpattern import *
from picowork.pfixedbackground import *
from tilemapgeneration import *
from tilemap import *
from portal import *
from coin import *
from monster import *


class PSceneVillage(PScene):
    def __init__(self):
        super().__init__()
        background_sky = PFixedBackground('skybox.png')
        self.add_element(background_sky)

        background = PScrollPattern('bg16_cloud_far.png', 3)
        background.set_position(Vector2(0, 12))
        self.add_element(background)

        background = PScrollPattern('bg_near.png', 2)
        background.set_position(Vector2(0, 10.5))
        self.add_element(background)

        gate = PSpriteObject('gate_parts.png')
        gate.set_position(Vector2(14.5, 10))
        self.add_element(gate)

        gate = PSpriteObject('gate_parts.png')
        gate.set_scale(Vector2(-1, 1))
        gate.set_position(Vector2(17.5, 10))
        self.add_element(gate)

        wagon = PSpriteObject('wagon.png')
        wagon.set_position(Vector2(12, 9.5))
        self.add_element(wagon)

        character = PSpriteObject("merchant_01.png")
        character.set_position(Vector2(19, 9.3))
        character.set_scale(Vector2(-1, 1))
        self.add_element(character)

        self.tilemap = Tilemap(32, 32, 'terr01_%02d.png', ['fill01b.png', 'fill01.png'])
        generate_tilemap_village(self.tilemap, 32, 32)
        self.add_element(self.tilemap)

        self.player = Player(self.tilemap)
        self.player.set_position(Vector2(9.5, 9))
        self.add_element(self.player, 2)

        import scenemanagement
        self.portal = Portal(self.player, scenemanagement.load_scene_dungeon)
        self.portal.set_position(Vector2(16, 9.5))
        self.add_element(self.portal)

        self.coins = []
        for x in range(20):
            coin = Coin(self.tilemap, self.player)
            coin.set_position(Vector2(x, 9.5))
            self.add_element(coin)
            self.coins.append(coin)

        self.monster = MonsterWizard(self.tilemap)
        self.monster.set_position(Vector2(16, 9.5))
        self.add_element(self.monster)

        camera._position = self.player.get_position()

    def update(self, delta_time):
        new_campos = camera._position + (self.player.get_position() - camera._position) * delta_time * 8
        hsw = camera._size * get_canvas_width() / get_canvas_height()
        new_campos = Vector2(clamp(hsw, new_campos.x, 32 - hsw), new_campos.y)
        magnitude = clamp(-0.5, (new_campos - camera._position).x * 50, 0.5)

        camera._position = new_campos
        camera._rotation = magnitude
        camera._size = 4 # + 4 * (t % 1) ** 0.05

        self.player.update(delta_time)
        self.portal.update(delta_time)

        for coin in self.coins:
            coin.update(delta_time)

        self.monster.update(delta_time)