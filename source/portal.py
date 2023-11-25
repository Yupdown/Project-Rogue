from picowork.pspriteobject import *
from picowork.psprite import *
from picowork.pinput import *

class Portal(PObject):
    sprites = None
    def __init__(self, player, portal_callback):
        super().__init__()
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

        self.player = player
        self.portal_callback = portal_callback
        self.time = 0
        self.near = False

    def update(self, delta_time):
        self.time += delta_time

        self.visual.set_rotation(self.time * -360)
        self.indicator.set_position(Vector2(0, sin(self.time * 10) * 0.05 + 1.2))

        near = (self.player.get_position() - self.get_position()).sqr_magnitude() < 1
        if near and not self.near:
            self.indicator.set_scale(Vector2(1, 2))
        self.indicator.set_scale(lerp(self.indicator.get_scale(), Vector2(1, 1) if near else Vector2(1, 0), delta_time * 24))
        if near and get_keydown(SDLK_w):
            self.portal_callback()
        self.near = near
        