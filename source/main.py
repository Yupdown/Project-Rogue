from pico2d import *

open_canvas(1280, 720)

flag = True
while flag:
    clear_canvas()
    update_canvas()

    events = get_events()
    for event in events:
        flag *= event.type != SDL_QUIT

close_canvas()