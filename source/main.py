import time
from picowork import picowork
from tilemap import *

time_begin = time.time()
tick = 0

def main_update():
    global tick

    time_current = time.time() - time_begin
    t = time_current if not picowork.pinput.get_button(SDL_BUTTON_LEFT) else time_current * 2
    # tile_map.set_rotation(sin(t * 20) * 10)
    camera._rotation = sin(t * 20) * 1
    camera._size = 5
    camera._position = Vector2(5, 5)

    tick += 1


picowork.initialize(1280, 720)
tilemap = Tilemap(10, 10, 'terr02_%02d.png', 'fill02.png')
picowork.current_scene.add_element(tilemap)

while picowork.event_update():
    main_update()
    picowork.render_update()

picowork.close()