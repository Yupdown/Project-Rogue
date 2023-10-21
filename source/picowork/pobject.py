from .putil import *


class PObject:
    def __init__(self):
        self._local_position = Vector2(0.0, 0.0)
        self._local_rotation = 0
        self._local_scale = Vector2(1.0, 1.0)
        self._concatenated_position = Vector2(0.0, 0.0)
        self._concatenated_rotation = 0
        self._concatenated_scale = Vector2(1.0, 1.0)
        self._elements = []

    def update_transform(self, parent):
        if parent is None:
            self._concatenated_position = self._local_position
            self._concatenated_rotation = self._local_rotation
            self._concatenated_scale = self._local_scale
        else:
            v = Vector2()
            r = radians(parent._concatenated_rotation)
            v.x = self._local_position.x * parent._concatenated_scale.x
            v.y = self._local_position.y * parent._concatenated_scale.y
            self._concatenated_position.x = cos(r) * v.x - sin(r) * v.y + parent._concatenated_position.x
            self._concatenated_position.y = sin(r) * v.x + cos(r) * v.y + parent._concatenated_position.y
            self._concatenated_rotation = parent._concatenated_rotation + self._local_rotation
            self._concatenated_scale.x = parent._concatenated_scale.x * self._local_scale.x
            self._concatenated_scale.y = parent._concatenated_scale.y * self._local_scale.y

    def draw(self, parent):
        self.update_transform(parent)
        self.on_draw()
        for element in self._elements:
            element.draw(self)

    def on_draw(self):
        pass

    def add_element(self, element):
        self._elements.append(element)

    def remove_element(self, element):
        if element in self._elements:
            self._elements.remove(element)

    def get_position(self):
        return self._local_position

    def set_position(self, value: Vector2):
        self._local_position = value

    def get_rotation(self):
        return self._local_rotation

    def set_rotation(self, value: float):
        self._local_rotation = value

    def get_scale(self):
        return self._local_scale

    def set_scale(self, value: Vector2):
        self._local_scale = value
