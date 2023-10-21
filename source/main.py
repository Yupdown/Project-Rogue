import time
import math
from picowork import picowork
from picowork.pspriteobject import *

time_begin = time.time()

def main_update():
    global parent
    time_current = time.time() - time_begin
    t = time_current

    parent.set_position(Vector2(640, 360))
    parent.set_rotation(t * 360)
    parent.set_scale(Vector2(cos(t) + 2, cos(t) + 2))


picowork.initialize(1280, 720)
parent = PObject()
for index in range(100):
    sprite = PSpriteObject('avatar02.png')
    sprite.set_position(Vector2((index // 10 - 4.5) * 100, (index % 10 - 4.5) * 100))
    sprite.set_scale(Vector2(0.25, 0.25))
    parent.add_element(sprite)
picowork.current_scene.add_element(parent)

while picowork.event_update():
    main_update()
    picowork.render_update()

picowork.close()