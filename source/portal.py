from picowork.pspriteobject import *
from picowork.psprite import *
from picowork.pinput import *
from worldobject import *

class Portal(WorldObject):
    sprites = None

    def __init__(self, tile_map, portal_callback):
        super().__init__(tile_map)
        self.collision_tag = 'portal'
        self.collision_bounds = (-0.5, -0.25, 0.5, 0.75)

        if Portal.sprites is None:
            image = get_image('portal_stripes3.png')
            Portal.sprites = [PSprite(image, (i % 2) * 512, (i // 2) * 512, 512, 512) for i in range(4)]

        self.visual = PSpriteObject(Portal.sprites[2])
        self.visual.set_position(Vector2(0, 0.25))
        self.visual.set_scale(Vector2(0.1, 0.1))
        self.add_element(self.visual)

        self.indicator = PSpriteObject('thin_btn_up.png')
        self.indicator.set_position(Vector2(0, 1.2))
        self.indicator.set_scale(Vector2(1, 0))
        self.add_element(self.indicator)

        self.portal_callback = portal_callback
        self.near = False

    def update(self, delta_time):
        super().update(delta_time)

        self.visual.set_rotation(self.time * -360)
        self.indicator.set_position(Vector2(0, sin(self.time * 10) * 0.05 + 1.2))

        near = len(self.get_parent().get_collision_objects_from_object('player', self)) > 0
        if near and not self.near:
            self.indicator.set_scale(Vector2(1, 2))
        self.indicator.set_scale(lerp(self.indicator.get_scale(), Vector2(1, 1) if near else Vector2(1, 0), delta_time * 24))
        if near and get_keydown(SDLK_w):
            sound = get_sound('Psychic_Soothe_Pulser_01a.wav')
            sound.set_volume(50)
            sound.play()
            self.portal_callback()
        self.near = near
