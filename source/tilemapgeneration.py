from collections import *
import random
import time
from pico2d import *
from math import *
from picowork.putil import *
from picowork.presource import *


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

    print('=== Dungeon Generation Procedure ===')
    print('Note: Rooms may not connect properly depending on the settled positions of the rooms')
    print()

    print('> Making virtual Rooms')
    print('Number of rooms: %d' % (room_count + 2))
    print()

    begin_room = Room(10, dungeon_height // 2 - 6, 16, 12)
    begin_room.name = 'START ROOM'
    begin_room.fixed = True
    begin_room.facet_from = (begin_room.w - 1, 1)

    end_room = Room(dungeon_width - 24 - 10, dungeon_height // 2 - 8, 24, 16)
    end_room.name = 'BOSS ROOM'
    end_room.fixed = True
    end_room.facet_to = (0, 1)

    for i in range(room_count):
        target = random.randrange(0, len(rooms))
        room = Room(
             0,
             0,
             rooms[target][0],
             rooms[target][1]
        )

        for x in range(room.w):
            for y in range(room.h):
                ch = rooms[target][2][y][x]
                if ch == 'T':
                    room.facet_to = (x, y)
                if ch == 'F':
                    room.facet_from = (x, y)

        room.x = random.randrange(0, dungeon_width - room.w)
        room.y = random.randrange(0, dungeon_height - room.h)
        room.name = 'ROOM %02d' % i
        room.target_room = target
        generated_rooms.append(room)

    generated_rooms.insert(0, begin_room)
    generated_rooms.append(end_room)

    sample_time = 2

    print('> Simulating to settle the rooms')
    print('Simulation time estimation: %ds' % sample_time)
    print()

    last_time = time.time()
    while sample_time > 0:
        yield
        t = time.time()
        delta_time = t - last_time
        sample_time -= delta_time
        last_time = t

        for i in range(len(generated_rooms)):
            generated_rooms[i].x = clamp(1, generated_rooms[i].x, w - 1 - generated_rooms[i].w)
            generated_rooms[i].y = clamp(1, generated_rooms[i].y, h - 1 - generated_rooms[i].h)

            x = generated_rooms[i].x + generated_rooms[i].w / 2
            y = generated_rooms[i].y + generated_rooms[i].h / 2

            d0 = x
            d1 = y
            d2 = x - dungeon_width
            d3 = y - dungeon_height

            mul = 10000 * delta_time
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

                sqr_magnitude = max(dx ** 2 + dy ** 2, 1)
                magnitude = sqrt(sqr_magnitude)
                ndx = clamp(-1, dx / magnitude, 1)
                ndy = clamp(-1, dy / magnitude, 1)

                if not generated_rooms[i].fixed:
                    generated_rooms[i].x += ndx / sqr_magnitude * mul
                    generated_rooms[i].y += ndy / sqr_magnitude * mul

                if not generated_rooms[j].fixed:
                    generated_rooms[j].x -= ndx / sqr_magnitude * mul
                    generated_rooms[j].y -= ndy / sqr_magnitude * mul

    print('> Validating positions of the rooms')

    remove_queue = []
    for room in generated_rooms:
        room.x = floor(room.x)
        room.y = floor(room.y)
        if room.x not in range(w - room.w) or room.y not in range(h - room.h):
            print('%s doesn\'t have a valid position! Removed from the list' % room.name)
            remove_queue.append(room)

    while remove_queue:
        generated_rooms.remove(remove_queue.pop())

    print('> Generating edges for MST')

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

    print('> Generating path mask map')

    edges.sort()
    nodes = dict()

    path_mask = [[True for _ in range(h)] for _ in range(w)]
    for room in generated_rooms:
        for x in range(max(0, room.x - 3), min(w, room.x + room.w + 3)):
            for y in range(max(0, room.y - 3), min(h, room.y + room.h + 3)):
                path_mask[x][y] = False
                if x <= room.x:
                    if room.facet_to and room.facet_to[0] == 0:
                        path_mask[x][y] = y == room.y + room.facet_to[1]
                    if room.facet_from and room.facet_from[0] == 0:
                        path_mask[x][y] = y == room.y + room.facet_from[1]
                if x + 1 >= room.x + room.w:
                    if room.facet_to and room.facet_to[0] == room.w - 1:
                        path_mask[x][y] = y == room.y + room.facet_to[1]
                    if room.facet_from and room.facet_from[0] == room.w - 1:
                        path_mask[x][y] = y == room.y + room.facet_from[1]

    print()
    print('> Connecting rooms')

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
            yield
        passages.append(point_from)
        yield

    print()
    print('> Filling the tilemap')

    for x in range(w):
        for y in range(h):
            tilemap.set_tile(x, y, 1)

    print('> Applying rooms to the tilemap')

    monsters = defaultdict(list)
    tile_to_room = [[None for _ in range(h)] for _ in range(w)]
    for room in generated_rooms:
        for x in range(max(0, room.x), min(w, room.x + room.w)):
            for y in range(max(0, room.y), min(h, room.y + room.h)):
                dx = x - room.x
                dy = y - room.y
                tile_to_room[x][y] = room
                if room.target_room < 0:
                    tilemap.set_tile(x, y, 0)
                else:
                    ch = rooms[room.target_room][2][dy][dx]
                    tilemap.set_tile(x, y, ch == '1')
                    import monster
                    if ch == 'A':
                        monsters[room].append((monster.MonsterSlime, x, y))
                    elif ch == 'B':
                        monsters[room].append((monster.MonsterGoblin, x, y))
                    elif ch == 'C':
                        monsters[room].append((monster.MonsterWizard, x, y))
    tilemap.metadata['rooms'] = generated_rooms
    tilemap.metadata['monsters'] = monsters
    tilemap.metadata['tile_to_room'] = tile_to_room

    print('> Applying passages to the tilemap')

    for passage in passages:
        tilemap.set_tile(passage[0], passage[1], -1)

    print()
    print('Dungeon Generation Procedure was done successfully')
    print()


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