from pscenevillage import *
from pscenedungeon import *
from picowork import picowork

loading_image = None
loading_font = None

def load_scene_village():
    draw_loading_image()
    update_canvas()
    picowork.change_scene(PSceneVillage())


def load_scene_dungeon():
    scene = PSceneDungeon()
    for _ in scene.generate_dungeon():
        clear_canvas()
        draw_loading_image()
        draw_generate_procedure()
        update_canvas()
    picowork.change_scene(scene)


def draw_loading_image():
    global loading_image
    global loading_font
    if not loading_image:
        loading_image = load_image('resource/splash_solid.png')
        # loading_image.opacify(64)
    if not loading_font:
        loading_font = load_font('DungGeunMo.ttf', 16)
    sw, sh =  get_canvas_width(), get_canvas_height()
    loading_image.draw_to_origin(0, 0, sw, sh)
    loading_font.draw(2, 10, "Loading Level ...", (255, 255, 255))