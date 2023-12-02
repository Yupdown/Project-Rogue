from collections import *
from picowork.pscene import *
from picowork.putil import *

class PSceneWorld(PScene):
    def __init__(self):
        super().__init__()

        self.world_objects = []
        self.collision_group = defaultdict(list)

    def add_world_object(self, world_object, layer = 0):
        self.add_element(world_object, layer)
        self.world_objects.append(world_object)
        if world_object.collision_bounds is not None:
            self.collision_group[world_object.collision_tag].append(world_object)

    def remove_world_object(self, world_object):
        self.remove_element(world_object)
        self.world_objects.remove(world_object)
        for group in self.collision_group.values():
            if world_object in group:
                group.remove(world_object)

    def update(self, delta_time):
        for world_object in self.world_objects:
            world_object.update(delta_time)

    def get_collision_objects(self, group, rect):
        result = []
        for world_object in self.collision_group[group]:
            v = world_object.get_position()
            r = world_object.collision_bounds
            object_rect = (v.x + r[0], v.y + r[1],  v.x + r[2], v.y + r[3])
            if rect_overlap(rect, object_rect):
                result.append(world_object)
        return result

    def get_collision_objects_from_object(self, group, world_object):
        v = world_object.get_position()
        r = world_object.collision_bounds
        self.get_collision_objects(group, (v.x + r[0], v.y + r[1], v.x + r[2], v.y + r[3]))