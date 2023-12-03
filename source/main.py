import time
from picowork import picowork
from tilemapgeneration import *
from player import *
from scenemanagement import *

picowork.initialize(1280, 720)
load_rooms()
load_scene_village()

while picowork.event_update():
    picowork.update()
    picowork.render_update()

picowork.close()