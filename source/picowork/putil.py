from math import *
from dataclasses import dataclass


@dataclass(frozen=True)
class Vector2:
    x: float = 0
    y: float = 0

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


def lerp(a, b, t):
    return a + (b - a) * t


def rect_overlap(lhs, rhs):
    if lhs[2] < rhs[0] or lhs[0] > rhs[2]:
        return False
    if lhs[3] < rhs[1] or lhs[1] > rhs[3]:
        return False
    return True
