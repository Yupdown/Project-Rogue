from pico2d import *

PIXEL_PER_UNIT = 32
_image_register = {}
_music_register = {}
_sound_register = {}

def _list_files_recursively(directory, filter, action):
    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith(filter):
                continue
            file_path = os.path.join(root, file)
            action(file_path)  # Replace this with your desired action
            yield file_path, file


def add_image(path):
    file_name = os.path.basename(path)
    image = load_image(path)
    _image_register[file_name] = image


def add_music(path):
    file_name = os.path.basename(path)
    sound = load_music(path)
    _music_register[file_name] = sound


def add_sound(path):
    file_name = os.path.basename(path)
    sound = load_wav(path)
    _sound_register[file_name] = sound


def load_images():
    directory = 'resource/image'
    return _list_files_recursively(directory, '.png', add_image)


def load_musics():
    directory = 'resource/music'
    return _list_files_recursively(directory, '', add_music)


def load_sounds():
    directory = 'resource/sound'
    return _list_files_recursively(directory, '', add_sound)


def get_image(file_name):
    return _image_register[file_name]


def get_music(file_name):
    return _music_register[file_name]


def get_sound(file_name):
    return _sound_register[file_name]
