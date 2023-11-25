from pscenevillage import *
from pscenedungeon import *
from picowork import picowork


def load_scene_village():
    picowork.change_scene(PSceneVillage())


def load_scene_dungeon():
    picowork.change_scene(PSceneDungeon())
