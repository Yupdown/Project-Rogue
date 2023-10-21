
class PScene:
    def __init__(self):
        self._elements = []

    def draw(self):
        for element in self._elements:
            element.draw(None)

    def add_element(self, element):
        self._elements.append(element)

    def remove_element(self, element):
        if element in self._elements:
            self._elements.remove(element)
