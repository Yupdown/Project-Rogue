from .pobject import *
from .presource import *


class PTextUIObject(PObject):
    font = None

    def __init__(self, text, color = (255, 255, 255)):
        super().__init__()
        self.text = text
        self.color = color
        if PTextUIObject.font is None:
            PTextUIObject.font = load_font('DungGeunMo.ttf', 32)

    def set_text(self, text):
        self.text = text

    def set_color(self, color):
        self.color = color

    def on_draw(self):
        v = self._concatenated_position
        PTextUIObject.font.draw(v.x, v.y, self.text, self.color)