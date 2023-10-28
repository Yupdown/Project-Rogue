import time
from pico2d import *
from picowork import picowork
from picowork.pspriteobject import *

time_begin = time.time()
objects = []


def main_update():
    global parent
    time_current = time.time() - time_begin
    t = time_current if not picowork.pinput.get_button(SDL_BUTTON_LEFT) else time_current * 2
    for index in range(21):
        objects[index].set_rotation(t * index * 30)
    # parent.set_scale(Vector2(cos(t) + 1.5, sin(t) + 1.5))
    # camera._rotation = sin(t * 20) * 10
    # camera._size = sin(t * 5) * 5


picowork.initialize(1280, 720)

parent = PObject()
objects.append(parent)
for index in range(20):
    rad = index / 10 * pi
    sprite = PSpriteObject('avatar02.png')
    sprite.set_position(Vector2(cos(rad), sin(rad)) * 5.0)
    sprite.set_scale(Vector2(0.5, 0.5))
    parent.add_element(sprite)
    objects.append(sprite)
picowork.current_scene.add_element(parent)

while picowork.event_update():
    main_update()
    picowork.render_update()

picowork.close()