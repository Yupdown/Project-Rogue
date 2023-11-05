from .pspriteobject import *
from .presource import *


class PFixedBackground(PSpriteObject):
    def __init__(self, image):
        super().__init__(image)

    def on_draw(self):
        self._image.draw_to_origin(0, 0, get_canvas_width(), get_canvas_height())