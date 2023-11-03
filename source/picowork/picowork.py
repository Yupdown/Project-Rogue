from pico2d import *
from .pscene import *
from . import pinput
from . import presource

current_scene = PScene()


def initialize(w, h):
    open_canvas(w, h)
    hide_lattice()

    font = load_font('DungGeunMo.ttf', 16)
    splash_image = load_image("resource/splash.png")

    for str_log in presource.load_images():
        clear_canvas()
        # splash_image.draw(w / 2, h / 2)
        font.draw(2, 10, str_log, (0, 0, 0))
        update_canvas()



def event_update():
    flag = True
    events = get_events()
    pinput.process_input(events)
    for event in events:
        flag *= event.type != SDL_QUIT
    return flag


def render_update():
    clear_canvas()
    current_scene.draw()
    update_canvas()


def close():
    close_canvas()