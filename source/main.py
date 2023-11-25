import time
from picowork import picowork
from tilemapgeneration import *
from player import *
from pscenevillage import *

picowork.initialize(1280, 720)
load_rooms()
picowork.change_scene(PSceneVillage())

while picowork.event_update():
    picowork.update()
    picowork.render_update()

picowork.close()