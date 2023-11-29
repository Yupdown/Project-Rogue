import random
from pico2d import *
from math import *
from picowork.putil import *


class Room:
    def __init__(self, x, y, w, h):
        self.name = 'ROOM'
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.facet_from = None
        self.facet_to = None
        self.fixed = False
        self.target_room = -1


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


def generate_tilemap(tilemap, w, h, room_count):
    global dungeon_width
    global dungeon_height
    global generated_rooms
    global passages

    dungeon_width = w
    dungeon_height = h
    generated_rooms = []
    passages = []

    begin_room = Room(10, 10, 16, 12)
    begin_room.name = 'START ROOM'
    begin_room.fixed = True
    begin_room.facet_from = (begin_room.w, 1)

    end_room = Room(dungeon_width - 24 - 10, dungeon_height - 16 - 10, 24, 16)
    end_room.name = 'BOSS ROOM'
    end_room.fixed = True
    end_room.facet_to = (-1, 1)

    for i in range(room_count):
        target = random.randrange(0, len(rooms))
        room = Room(
             0,
             0,
             rooms[target][0],
             rooms[target][1]
        )
        room.x = random.randrange(0, dungeon_width - room.w)
        room.y = random.randrange(0, dungeon_height - room.h)
        room.name = 'ROOM %02d' % i
        room.facet_to = (-1, 2)
        room.facet_from = (room.w, 2)
        room.target_room = target
        generated_rooms.append(room)

    generated_rooms.insert(0, begin_room)
    generated_rooms.append(end_room)

    for sample in range(1 << 12):
        for i in range(len(generated_rooms)):

            x = generated_rooms[i].x + generated_rooms[i].w / 2
            y = generated_rooms[i].y + generated_rooms[i].h / 2

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

            if not generated_rooms[i].fixed:
                generated_rooms[i].x += force.x
                generated_rooms[i].y += force.y

            for j in range(i + 1, len(generated_rooms)):
                xp = generated_rooms[j].x + generated_rooms[j].w / 2
                yp = generated_rooms[j].y + generated_rooms[j].h / 2

                dx = x - xp
                dy = y - yp

                sqr_magnitude = dx ** 2 + dy ** 2
                magnitude = sqrt(sqr_magnitude)
                ndx = clamp(-1, dx / magnitude, 1)
                ndy = clamp(-1, dy / magnitude, 1)

                if not generated_rooms[i].fixed:
                    generated_rooms[i].x += ndx / sqr_magnitude * mul
                    generated_rooms[i].y += ndy / sqr_magnitude * mul

                if not generated_rooms[j].fixed:
                    generated_rooms[j].x -= ndx / sqr_magnitude * mul
                    generated_rooms[j].y -= ndy / sqr_magnitude * mul
        yield None

    for room in generated_rooms:
        room.x = floor(room.x)
        room.y = floor(room.y)

    edges = []
    for i in range(len(generated_rooms)):
        if generated_rooms[i].facet_from is None:
            continue
        for j in range(len(generated_rooms)):
            if i == j:
                continue
            if generated_rooms[j].facet_to is None:
                continue
            dx = (generated_rooms[j].x + generated_rooms[j].facet_to[0]) - (generated_rooms[i].x + generated_rooms[i].facet_from[0])
            dy = (generated_rooms[j].y + generated_rooms[j].facet_to[1]) - (generated_rooms[i].y + generated_rooms[i].facet_from[1])
            edges.append((abs(dx) + abs(dy), i, j))

    edges.sort()
    nodes = dict()

    path_mask = [[True for _ in range(h)] for _ in range(w)]
    for room in generated_rooms:
        for x in range(max(0, room.x - 1), min(w, room.x + room.w + 1)):
            for y in range(max(0, room.y - 1), min(h, room.y + room.h + 1)):
                path_mask[x][y] = False
        if room.facet_to is not None:
            path_mask[room.x + room.facet_to[0]][room.y + room.facet_to[1]] = True

    for edge in edges:
        i = edge[1]
        j = edge[2]

        # Find LCA
        pi = i
        pj = j
        while pi in nodes:
            pi = nodes[pi]
        while pj in nodes:
            pj = nodes[pj]
        if pi == pj:
            continue

        point_from = (generated_rooms[i].x + generated_rooms[i].facet_from[0], generated_rooms[i].y + generated_rooms[i].facet_from[1])
        point_to = (generated_rooms[j].x + generated_rooms[j].facet_to[0], generated_rooms[j].y + generated_rooms[j].facet_to[1])

        bfs_memo = [[None for _ in range(h)] for _ in range(w)]
        queue_bfs = [point_from]

        while queue_bfs:
            node_current = queue_bfs.pop(0)
            if node_current == point_to:
                break
            offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(offsets)
            for offset in offsets:
                next_x = node_current[0] + offset[0]
                next_y = node_current[1] + offset[1]
                if next_x not in range(w) or next_y not in range(h):
                    continue
                if not path_mask[next_x][next_y]:
                    continue
                if bfs_memo[next_x][next_y] is not None:
                    continue
                bfs_memo[next_x][next_y] = node_current
                queue_bfs.append((next_x, next_y))
        else:
            print('Couldn\'t connect! ' + generated_rooms[i].name + ' - ' + generated_rooms[j].name)
            continue

        # Union LCA
        nodes[pj] = pi

        print('Connect ' + generated_rooms[i].name + ' - ' + generated_rooms[j].name)

        passage = point_to
        while passage != point_from:
            passages.append(passage)
            passage = bfs_memo[passage[0]][passage[1]]
            yield None
        passages.append(point_from)

    for x in range(w):
        for y in range(h):
            tilemap.set_tile(x, y, 1)

    for room in generated_rooms:
        for x in range(max(0, room.x), min(w, room.x + room.w)):
            for y in range(max(0, room.y), min(h, room.y + room.h)):
                dx = x - room.x
                dy = y - room.y
                if room.target_room < 0:
                    tilemap.set_tile(x, y, 0)
                else:
                    tilemap.set_tile(x, y, rooms[room.target_room][2][dy][dx] != '0')

    for passage in passages:
        tilemap.set_tile(passage[0], passage[1], -1)

    # ex = None
    # for i in range(5):
    #     room = rooms[random.randrange(len(rooms))]
    #     sx = i * 16 + 8
    #     sy = 8
    #
    #     if ex is not None:
    #         for x in range(ex, sx):
    #                 tilemap.set_tile(x, sy + 2, False)
    #
    #     ex = sx + room[0]
    #     for dx in range(room[0]):
    #         for dy in range(room[1]):
    #             x = sx + dx
    #             y = sy + dy
    #             if room[2][dy][dx] == '0':
    #                 tilemap.set_tile(x, y, False)


def draw_generate_procedure():
    global font
    if font is None:
        font = load_font('DungGeunMo.ttf', 16)
    scale = 320 / dungeon_height
    sw, sh = get_canvas_width(), get_canvas_height()
    draw_rectangle(
        sw // 2 - dungeon_width * scale // 2,
        sh // 2 - dungeon_height * scale // 2,
        sw // 2 + dungeon_width * scale // 2,
        sh // 2 + dungeon_height * scale // 2
    )

    for room in generated_rooms:
        x = room.x - dungeon_width / 2
        y = room.y - dungeon_height / 2
        draw_rectangle(
            sw // 2 + floor(x) * scale,
            sh // 2 + floor(y) * scale,
            sw // 2 + floor(x + room.w) * scale,
            sh // 2 + floor(y + room.h) * scale
        )
        font.draw(
            sw // 2 + floor(x) * scale + 2,
            sh // 2 + floor(y + room.h) * scale - 6,
            room.name, (255, 0, 0))

    for passage in passages:
        x = passage[0] - dungeon_width / 2
        y = passage[1] - dungeon_height / 2
        draw_rectangle(
            sw // 2 + floor(x) * scale,
            sh // 2 + floor(y) * scale,
            sw // 2 + floor(x + 1) * scale,
            sh // 2 + floor(y + 1) * scale
        )

def generate_tilemap_village(tilemap, w, h):
    for x in range(w):
        for y in range(h):
            if y > 8:
                continue
            tilemap.set_tile(x, y, True)