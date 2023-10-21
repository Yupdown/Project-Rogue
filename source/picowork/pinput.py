from pico2d import *

_key_state = {}
_button_state = {}
_time = 0


def process_input(events):
    global _time
    _time += 1
    for event in events:
        if event.type == SDL_KEYDOWN or event.type == SDL_KEYUP:
            _key_state[event.key] = (event.type, _time)
        elif event.type == SDL_MOUSEBUTTONDOWN or event.type == SDL_MOUSEBUTTONUP:
            _button_state[event.button] = (event.type, _time)


def get_key(key):
    if key not in _key_state:
        return False
    return _key_state[key][0] == SDL_KEYDOWN


def get_keydown(key):
    if key not in _key_state:
        return False
    return _key_state[key][0] == SDL_KEYDOWN and _key_state[key][1] == _time


def get_keyup(key):
    if key not in _key_state:
        return False
    return _key_state[key][0] == SDL_KEYUP and _key_state[key][1] == _time


def get_button(button):
    if button not in _button_state:
        return False
    return _button_state[button][0] == SDL_MOUSEBUTTONDOWN


def get_buttondown(button):
    if button not in _button_state:
        return False
    return _button_state[button][0] == SDL_MOUSEBUTTONDOWN and _button_state[button][1] == _time


def get_buttonup(button):
    if button not in _button_state:
        return False
    return _button_state[button][0] == SDL_MOUSEBUTTONUP and _button_state[button][1] == _time
