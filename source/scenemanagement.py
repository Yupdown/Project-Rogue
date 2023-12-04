from pscenevillage import *
from pscenedungeon import *
from picowork import picowork

loading_image = None
loading_font = None

def load_scene_village():
    draw_loading_image()
    update_canvas()
    picowork.change_scene(PSceneVillage())

    global global_bgm
    global_bgm = get_music('music01.mp3')
    global_bgm.set_volume(50)
    global_bgm.repeat_play()


def load_scene_dungeon():
    scene = PSceneDungeon()
    loading_images = [PSprite(get_image('uiloading.png'), i % 4 * 18, i // 4 * 18, 18, 18) for i in range(8)]
    cnt = 0

    global global_bgm
    if global_bgm:
        global_bgm.stop()

    for _ in scene.generate_dungeon():
        clear_canvas()
        draw_loading_image()
        loading_images[cnt // 16 % 8].draw(160, 12)
        cnt += 1
        draw_generate_procedure()
        update_canvas()
    scene.on_generate_dungeon()
    picowork.change_scene(scene)

    global_bgm = get_music('music02.mp3')
    global_bgm.set_volume(50)
    global_bgm.repeat_play()


def draw_loading_image():
    global loading_image
    global loading_font
    if not loading_image:
        loading_image = get_image('splash_solid.png')
        # loading_image.opacify(64)
    if not loading_font:
        loading_font = load_font('DungGeunMo.ttf', 16)
    sw, sh = get_canvas_width(), get_canvas_height()
    loading_image.draw_to_origin(0, 0, sw, sh)
    loading_font.draw(2, 10, "Loading Level ...", (255, 255, 255))