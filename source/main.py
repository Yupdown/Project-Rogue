import time
from picowork import picowork
from tilemap import *
from player import *
from tilemapgeneration import *
from picowork.pspriteobject import *
from picowork.pscrollpattern import *
from picowork.pfixedbackground import *

time_begin = time.time()
time_current = 0
tick = 0

def main_update():
    global tick
    global player
    global time_current

    time_new = time.time() - time_begin
    delta_time = min(time_new - time_current, 0.1)
    time_current = time_new

    t = time_current if not picowork.pinput.get_button(SDL_BUTTON_LEFT) else time_current * 2

    new_campos = camera._position + (player.get_position() - camera._position) * delta_time * 8
    magnitude = clamp(-0.5, (new_campos - camera._position).x * 50, 0.5)

    camera._position = new_campos
    camera._rotation = magnitude
    camera._size = 1 + 4 * (t % 1) ** 0.05
    camera._rotation = sin(t * 40) * 6 * (1 - (t % 1)) ** 4

    player.update(delta_time)

    tick += 1


picowork.initialize(1280, 720)
load_rooms()

background_sky = PFixedBackground('skybox.png')
picowork.current_scene.add_element(background_sky)

background = PScrollPattern('bg01_far.png', 3)
background.set_position(Vector2(0, 14))
picowork.current_scene.add_element(background)

background_near0 = PScrollPattern('bg01_mid.png', 2.5)
background_near0.set_position(Vector2(0, 12))
picowork.current_scene.add_element(background_near0)

background_near1 = PScrollPattern('bg01_mid.png', 2.0)
background_near1.set_position(Vector2(0, 11))
picowork.current_scene.add_element(background_near1)

background_near2 = PScrollPattern('bg01_mid.png', 1.75)
background_near2.set_position(Vector2(0, 10))
picowork.current_scene.add_element(background_near2)

tilemap = Tilemap(256, 32, 'terr02_%02d.png', 'fill02.png')
generate_tilemap(tilemap, 256, 32)
picowork.current_scene.add_element(tilemap)

player = Player(tilemap)
player.set_position(Vector2(9.5, 9.5))
picowork.current_scene.add_element(player)
camera._position = Vector2(10, 5)

while picowork.event_update():
    main_update()
    picowork.render_update()

picowork.close()