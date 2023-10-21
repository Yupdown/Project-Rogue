from pico2d import *
from .pscene import *
from . import pinput
from . import presource

current_scene = PScene()


def initialize(w, h):
    open_canvas(w, h)
    presource.load_images()


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