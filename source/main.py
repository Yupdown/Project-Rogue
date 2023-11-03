import time
from picowork import picowork
from tilemap import *
from player import *
from picowork.pspriteobject import *

time_begin = time.time()
time_current = 0
tick = 0

def main_update():
    global tick
    global player
    global time_current

    global background
    global background_near

    time_new = time.time() - time_begin
    delta_time = min(time_new - time_current, 0.1)
    time_current = time_new

    t = time_current if not picowork.pinput.get_button(SDL_BUTTON_LEFT) else time_current * 2
    # tile_map.set_rotation(sin(t * 20) * 10)
    # camera._rotation = sin(t * 10)
    # camera._size = 5 + sin(t * 40) * 0.1

    new_campos = camera._position + (player.get_position() - camera._position) * delta_time * 8
    magnitude = (new_campos - camera._position).x * 50

    camera._size = 3.5
    camera._position = new_campos
    camera._rotation = magnitude

    player.update(delta_time)

    background.set_position(Vector2(background.get_position().x, camera._position.y * 0.9))
    background_near.set_position(Vector2(background_near.get_position().x, camera._position.y - 1))

    tick += 1


picowork.initialize(1280, 720)

background = PSpriteObject('bg01_far.png')
background.set_position(Vector2(16, 10))
picowork.current_scene.add_element(background)

background_near = PSpriteObject('bg01_mid.png')
background_near.set_position(Vector2(16, 9))
picowork.current_scene.add_element(background_near)

tilemap = Tilemap(32, 20, 'terr02_%02d.png', 'fill02.png')
for x in range(32):
    for y in range(20):
        dist = sqrt((x - 15.5) ** 2 * 0.5 + (y - 9.5) ** 2)
        cond = dist > 5.5
        tilemap.set_tile(x, y, cond)
picowork.current_scene.add_element(tilemap)

player = Player(tilemap)
player.set_position(Vector2(16, 5))
picowork.current_scene.add_element(player)
camera._position = Vector2(10, 5)

while picowork.event_update():
    main_update()
    picowork.render_update()

picowork.close()