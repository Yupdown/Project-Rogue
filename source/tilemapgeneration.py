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
        self.target_preset = None

    def get_facet_positions(self):
        result = []
        if self.facet_to is not None:
            result.append((self.x + self.facet_to[0], self.y + self.facet_to[1]))
        if self.facet_from is not None:
            result.append((self.x + self.facet_from[0], self.y + self.facet_from[1]))
        return result

    def load_from_preset(self, preset):
        self.w = preset[0]
        self.h = preset[1]
        for x in range(self.w):
            for y in range(self.h):
                ch = preset[2][y][x]
                if ch == 'T':
                    self.facet_to = (x, y)
                if ch == 'F':
                    self.facet_from = (x, y)
        self.target_preset = preset


rooms = []
font = None
images = None

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

    begin_room = Room(10, dungeon_height // 2 - 6, 0, 0)
    begin_room.load_from_preset(rooms[0])
    begin_room.name = 'START ROOM'
    begin_room.fixed = True

    end_room = Room(0, dungeon_height // 2 - 8, 0, 0)
    end_room.load_from_preset(rooms[1])
    end_room.x = dungeon_width - end_room.w - 10
    end_room.name = 'BOSS ROOM'
    end_room.fixed = True

    for i in range(room_count):
        target = i % (len(rooms) - 2) + 2
        room = Room(0, 0, 0, 0)
        room.load_from_preset(rooms[target])

        room.x = random.randrange(0, dungeon_width - room.w)
        room.y = random.randrange(0, dungeon_height - room.h)
        room.name = 'ROOM %02d' % i
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

    path_mask = [[0 for _ in range(h)] for _ in range(w)]
    for room in generated_rooms:
        for x in range(max(0, room.x - 3), min(w, room.x + room.w + 3)):
            for y in range(max(0, room.y - 3), min(h, room.y + room.h + 3)):
                path_mask[x][y] = 1 if max(0, room.x - x) + max(0, room.y - y) + max(0, x + 1 - room.x - room.w) + max(0, y + 1 - room.y - room.h) > 1 else 2
                if x <= room.x:
                    if room.facet_to and room.facet_to[0] == 0 and y == room.y + room.facet_to[1]:
                        path_mask[x][y] = 0
                    if room.facet_from and room.facet_from[0] == 0 and y == room.y + room.facet_from[1]:
                        path_mask[x][y] = 0
                if x + 1 >= room.x + room.w:
                    if room.facet_to and room.facet_to[0] == room.w - 1 and y == room.y + room.facet_to[1]:
                        path_mask[x][y] = 0
                    if room.facet_from and room.facet_from[0] == room.w - 1 and y == room.y + room.facet_from[1]:
                        path_mask[x][y] = 0

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

        for threshold in range(1, 3):
            bfs_memo = [[None for _ in range(h)] for _ in range(w)]
            queue_bfs = [point_from]
            flag = False
            while queue_bfs:
                node_current = queue_bfs.pop(0)
                if node_current == point_to:
                    flag = True
                    break
                offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                random.shuffle(offsets)
                for offset in offsets:
                    next_x = node_current[0] + offset[0]
                    next_y = node_current[1] + offset[1]
                    if next_x not in range(w) or next_y not in range(h):
                        continue
                    if path_mask[next_x][next_y] >= threshold:
                        continue
                    if bfs_memo[next_x][next_y] is not None:
                        continue
                    bfs_memo[next_x][next_y] = node_current
                    queue_bfs.append((next_x, next_y))
            if flag:
                break
            print('Connection Fallback')
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
                ch = room.target_preset[2][dy][dx]
                tilemap.set_tile(x, y, ch == '1')
                import monster
                if ch == 'A':
                    monsters[room].append((monster.MonsterSlime, x, y))
                elif ch == 'B':
                    monsters[room].append((monster.MonsterGoblin, x, y))
                elif ch == 'C':
                    monsters[room].append((monster.MonsterWizard, x, y))
        for facet in room.get_facet_positions():
            tile_to_room[facet[0]][facet[1]] = None
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
    global images
    global font
    if images is None:
        images = [get_image('splash_solid.png'), get_image('splash_solid_white.png')]
    if font is None:
        font = load_font('DungGeunMo.ttf', 16)
    scale = 320 / dungeon_height
    sw, sh = get_canvas_width(), get_canvas_height()
    # images[1].draw(sw // 2, sh // 2, dungeon_width * scale, dungeon_height * scale)

    for room in generated_rooms:
        x = room.x - dungeon_width / 2
        y = room.y - dungeon_height / 2
        images[1].draw_to_origin(
            sw // 2 + floor(x) * scale,
            sh // 2 + floor(y) * scale,
            floor(room.w) * scale,
            floor(room.h) * scale
        )
        font.draw(
            sw // 2 + floor(x) * scale,
            sh // 2 + floor(y + room.h) * scale + 6,
            room.name, (255, 255, 255))

    for passage in passages:
        x = passage[0] - dungeon_width / 2
        y = passage[1] - dungeon_height / 2
        images[1].draw_to_origin(
            sw // 2 + floor(x) * scale,
            sh // 2 + floor(y) * scale,
            scale + 1,
            scale + 1
        )

def generate_tilemap_village(tilemap, w, h):
    for x in range(w):
        for y in range(h):
            if y > 8:
                continue
            tilemap.set_tile(x, y, True)