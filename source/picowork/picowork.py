import time
from pico2d import *
from .pscene import *
from . import pinput
from . import presource

time_begin = time.time()
time_current = 0
quit_event = False

def initialize(w, h):
    open_canvas(w, h)
    hide_lattice()

    font = load_font('DungGeunMo.ttf', 16)
    splash_image = load_image("resource/splash.png")

    for path, file in presource.load_images():
        clear_canvas()
        splash_image.draw(w / 2, h / 2)
        font.draw(2, 10, 'Load: image - ' + path, (0, 0, 0))
        presource.get_image(file).draw(get_canvas_width() - 30, 30, 50, 50)
        update_canvas()

    for path, file in presource.load_musics():
        clear_canvas()
        splash_image.draw(w / 2, h / 2)
        font.draw(2, 10, 'Load: music - ' + path, (0, 0, 0))
        update_canvas()

    for path, file in presource.load_sounds():
        clear_canvas()
        splash_image.draw(w / 2, h / 2)
        font.draw(2, 10, 'Load: sound - ' + path, (0, 0, 0))
        update_canvas()


def event_update():
    global quit_event
    flag = True
    events = get_events()
    pinput.process_input(events)
    for event in events:
        flag *= event.type != SDL_QUIT
    return flag and not quit_event


def update():
    global time_current
    time_new = time.time() - time_begin
    delta_time = min(time_new - time_current, 0.1)
    time_current = time_new
    if current_scene is not None:
        current_scene.update(delta_time)

def render_update():
    clear_canvas()
    current_scene.draw()
    update_canvas()


def quit_application():
    global quit_event
    quit_event = True


def close():
    close_canvas()


def change_scene(scene):
    global current_scene
    current_scene = scene


change_scene(PScene())
