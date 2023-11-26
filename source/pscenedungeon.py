from picowork.pscene import *
from picowork.pspriteobject import *
from picowork.pscrollpattern import *
from picowork.pfixedbackground import *
from tilemapgeneration import *
from tilemap import *
from portal import *


class PSceneDungeon(PScene):
    def __init__(self):
        super().__init__()
        background_sky = PFixedBackground('skybox.png')
        self.add_element(background_sky)

        background = PScrollPattern('bg01_far.png', 3)
        background.set_position(Vector2(0, 14))
        self.add_element(background)

        background_near0 = PScrollPattern('bg01_mid.png', 2.5)
        background_near0.set_position(Vector2(0, 12))
        self.add_element(background_near0)

        background_near1 = PScrollPattern('bg01_mid.png', 2.0)
        background_near1.set_position(Vector2(0, 11))
        self.add_element(background_near1)

        background_near2 = PScrollPattern('bg01_mid.png', 1.75)
        background_near2.set_position(Vector2(0, 10))
        self.add_element(background_near2)

        self.tilemap = Tilemap(256, 32, 'terr02_%02d.png', 'fill02.png')
        generate_tilemap(self.tilemap, 256, 32)
        self.add_element(self.tilemap)

        self.player = Player(self.tilemap)
        self.player.set_position(Vector2(9.5, 9))
        self.add_element(self.player, 2)

        import scenemanagement
        self.portal = Portal(self.player, scenemanagement.load_scene_village)
        self.portal.set_position(Vector2(10, 9.5))
        self.add_element(self.portal)

        camera._position = self.player.get_position()

    def update(self, delta_time):
        new_campos = camera._position + (self.player.get_position() - camera._position) * delta_time * 8

        magnitude = clamp(-0.5, (new_campos - camera._position).x * 50, 0.5)

        camera._position = new_campos
        camera._rotation = magnitude
        camera._size = 4 # + 4 * (t % 1) ** 0.05

        self.player.update(delta_time)
        self.portal.update(delta_time)