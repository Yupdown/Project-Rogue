from math import *
from dataclasses import dataclass


@dataclass
class Vector2:
    x: float = 0
    y: float = 0

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __floor__(self):
        return Vector2(floor(self.x), floor(self.y))

    def __ceil__(self):
        return Vector2(ceil(self.x), ceil(self.y))

    def sqr_magnitude(self):
        return self.x ** 2 + self.y ** 2

    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2)