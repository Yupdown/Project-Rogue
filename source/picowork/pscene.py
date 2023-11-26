
class PScene:
    def __init__(self):
        self._elements = {}

    def update(self, delta_time):
        pass

    def draw(self):
        for layer in self._elements.values():
            for element in layer:
                element.draw(None, False)

    def add_element(self, element, layer = 0):
        if layer not in self._elements:
            self._elements[layer] = []
            self._elements = dict(sorted(self._elements.items()))
        self._elements[layer].append(element)
        element._parent = self

    def remove_element(self, element):
        for layer in self._elements.values():
            if element in layer:
                layer.remove(element)
                element._parent = None