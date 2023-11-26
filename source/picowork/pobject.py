from .putil import *


class PObject:
    def __init__(self):
        self._local_position = Vector2(0, 0)
        self._local_rotation = 0
        self._local_scale = Vector2(1, 1)
        self._concatenated_position = Vector2(0, 0)
        self._concatenated_rotation = 0
        self._concatenated_scale = Vector2(1, 1)
        self._parent = None
        self._elements = []
        self._transform_dirty = True

    def validate_transform(self, parent):
        if parent is None:
            self._concatenated_position = self._local_position
            self._concatenated_rotation = self._local_rotation
            self._concatenated_scale = self._local_scale
        else:
            v = Vector2(self._local_position.x * parent._concatenated_scale.x, self._local_position.y * parent._concatenated_scale.y)
            if parent._concatenated_rotation != 0:
                r = radians(parent._concatenated_rotation)
                self._concatenated_position = Vector2(cos(r) * v.x - sin(r) * v.y, sin(r) * v.x + cos(r) * v.y) + parent._concatenated_position
            else:
                self._concatenated_position = v + parent._concatenated_position
            sign = 1 if parent._concatenated_scale.x * parent._concatenated_scale.y >= 0 else -1
            self._concatenated_rotation = parent._concatenated_rotation + self._local_rotation * sign
            self._concatenated_scale = Vector2(parent._concatenated_scale.x * self._local_scale.x, parent._concatenated_scale.y * self._local_scale.y)
        self._transform_dirty = False

    def draw(self, parent, force_validate = True):
        need_validate = self._transform_dirty or force_validate
        if need_validate:
            self.validate_transform(parent)
        self.on_draw()
        for element in self._elements:
            element.draw(self, need_validate)

    def on_draw(self):
        pass

    def add_element(self, element):
        self._elements.append(element)
        element._parent = self

    def remove_element(self, element):
        if element in self._elements:
            self._elements.remove(element)
            element._parent = None

    def remove_from_parent(self):
        self._parent.remove_element(self)

    def get_parent(self):
        return self._parent

    def get_position(self):
        return self._local_position

    def set_position(self, value: Vector2):
        self._local_position = value
        self._transform_dirty = True

    def get_rotation(self):
        return self._local_rotation

    def set_rotation(self, value: float):
        self._local_rotation = (value + 180) % 360 - 180
        self._transform_dirty = True

    def get_scale(self):
        return self._local_scale

    def set_scale(self, value: Vector2):
        self._local_scale = value
        self._transform_dirty = True
