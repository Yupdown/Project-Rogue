import random
from pico2d import *
from math import *
from picowork.putil import *

rooms = []
font = None

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
    global dungeon_width
    global dungeon_height
    global generated_rooms

    dungeon_width = w
    dungeon_height = h
    generated_rooms = []

    for i in range(5):
        generated_rooms.append([
             random.randrange(0, dungeon_width // 2),
             random.randrange(0, dungeon_height // 2),
            random.randint(16, 24),
            random.randint(12, 16)
        ])

    for sample in range(1 << 12):
        yield None
        for i in range(len(generated_rooms)):
            x = generated_rooms[i][0] + generated_rooms[i][2] / 2
            y = generated_rooms[i][1] + generated_rooms[i][3] / 2

            d0 = x
            d1 = y
            d2 = x - dungeon_width
            d3 = y - dungeon_height

            mul = 10
            force = Vector2(0, 0)
            force += Vector2(1, 0) / d0 ** 2 * mul
            force += Vector2(0, 1) / d1 ** 2 * mul
            force += Vector2(-1, 0) / d2 ** 2 * mul
            force += Vector2(0, -1) / d3 ** 2 * mul

            generated_rooms[i][0] += force.x
            generated_rooms[i][1] += force.y

            for j in range(i + 1, len(generated_rooms)):
                xp = generated_rooms[j][0] + generated_rooms[j][2] / 2
                yp = generated_rooms[j][1] + generated_rooms[j][3] / 2

                dx = x - xp
                dy = y - yp

                sqr_magnitude = dx ** 2 + dy ** 2
                magnitude = sqrt(sqr_magnitude)
                ndx = dx / magnitude
                ndy = dy / magnitude

                generated_rooms[j][0] -= ndx / sqr_magnitude * mul
                generated_rooms[j][1] -= ndy / sqr_magnitude * mul
                generated_rooms[i][0] += ndx / sqr_magnitude * mul
                generated_rooms[i][1] += ndy / sqr_magnitude * mul

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


def draw_generate_procedure():
    global font
    if font is None:
        font = load_font('DungGeunMo.ttf', 16)
    scale = 320 / dungeon_height
    sw, sh =  get_canvas_width(), get_canvas_height()
    draw_rectangle(
        sw // 2 - dungeon_width * scale // 2,
        sh // 2 - dungeon_height * scale // 2,
        sw // 2 + dungeon_width * scale // 2,
        sh // 2 + dungeon_height * scale // 2
    )
    for room in generated_rooms:
        x = room[0] - dungeon_width / 2
        y = room[1] - dungeon_height / 2
        draw_rectangle(
            sw // 2 + floor(x) * scale,
            sh // 2 + floor(y) * scale,
            sw // 2 + floor(x + room[2]) * scale,
            sh // 2 + floor(y + room[3]) * scale,
        )
        font.draw(
            sw // 2 + floor(x) * scale + 2,
            sh // 2 + floor(y) * scale + 8,
            'room', (255, 0, 0))

def generate_tilemap_village(tilemap, w, h):
    for x in range(w):
        for y in range(h):
            if y > 8:
                continue
            tilemap.set_tile(x, y, True)