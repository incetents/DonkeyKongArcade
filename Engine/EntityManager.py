
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# System for organizing, updating and drawing all entities for a scene
from typing import *
from Engine.Entity import *

_instance = None

class EntityManager_2D:
    def __init__(self):
        self._entities: Dict[str, Entity_2D] = {}

    @staticmethod
    def get_singleton():
        global _instance
        if _instance is None:
            _instance = EntityManager_2D()
        return _instance

    def clear(self):
        self._entities.clear()

    def add_entity(self, _ent: Entity_2D):
        self._entities[_ent.name] = _ent

    def update(self, delta_time: float):
        e: Entity_2D
        for e in self._entities.items():
            if e.enabled is True:
                e.update(delta_time)

    def draw(self):
        e: Entity_2D
        for e in self._entities.items():
            if e.enabled is True:
                e.draw()