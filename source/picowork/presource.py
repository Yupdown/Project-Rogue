from pico2d import *

PIXEL_PER_UNIT = 100
_image_register = {}

def _list_files_recursively(directory, action):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            action(file_path)  # Replace this with your desired action


def add_image(path):
    file_name = os.path.basename(path)
    image = load_image(path)
    _image_register[file_name] = image
    print('Load: image - ' + file_name + ' (' + path + ')')


def load_images():
    directory = 'resource'
    _list_files_recursively(directory, add_image)


def get_image(file_name):
    return _image_register[file_name]