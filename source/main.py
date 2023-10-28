import time
from pico2d import *
from picowork import picowork
from picowork.presource import *
from picowork.pspriteobject import *
from picowork.ptilemapobject import *

time_begin = time.time()
tick = 0

def main_update():
    global parent
    global tile_map
    global tick
    global img

    time_current = time.time() - time_begin
    t = time_current if not picowork.pinput.get_button(SDL_BUTTON_LEFT) else time_current * 2
    # tile_map.set_rotation(sin(t * 20) * 10)
    # camera._rotation = sin(t * 20) * 10
    camera._size = (sin(t * 3) + 1) * 10

    posx = int(tick % 10)
    posy = int(tick / 10 % 10)
    tile_map.set_tile(posx, posy, img if tile_map.get_tile(posx, posy) is None else None)
    tick += 1


picowork.initialize(1280, 720)

tile_map = PTileMapObject(10, 10, 1)
tile_map.set_position(Vector2(1.0, 0.0))
picowork.current_scene.add_element(tile_map)
img = get_image('terr02b.png').clip_image(0, 32, 8, 8)

parent = PObject()

while picowork.event_update():
    main_update()
    picowork.render_update()

picowork.close()