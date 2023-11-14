import random
from math import *

rooms = []

def load_rooms():
    file = open('resource/rooms.txt', 'r')
    n = int(file.readline())
    for _ in range(n):
        w, h = map(int, file.readline().split())
        m = []
        for _ in range(h):
            s = file.readline()
            m.insert(0, list(s))
        rooms.append((w, h, m))


def generate_tilemap(tilemap, w, h):
    for x in range(w):
        for y in range(h):
            tilemap.set_tile(x, y, True)

    ex = None
    for i in range(5):
        room = rooms[random.randrange(len(rooms))]
        sx = i * 16 + 8
        sy = 8

        if ex is not None:
            for x in range(ex, sx):
                    tilemap.set_tile(x, sy + 2, False)

        ex = sx + room[0]
        for dx in range(room[0]):
            for dy in range(room[1]):
                x = sx + dx
                y = sy + dy
                if room[2][dy][dx] == '0':
                    tilemap.set_tile(x, y, False)