
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# System for organizing, updating and drawing all entities for a scene
from typing import *
from Engine.Entity import *
from Engine.SpriteBatch import *
from Engine.CollisionManager import *

_instance = None

class EntityManager_2D:
    def __init__(self):
        self._dynamic_entities: Dict[str, Entity_2D] = {}
        self._entities: Dict[str, Entity_2D] = {}
        self._remove_entity_list: List[Entity_2D] = []

        self._batches: Dict[str, SpriteBatch] = {}
        self._remove_batch_list: List[SpriteBatch] = []

    @staticmethod
    def get_singleton():
        global _instance
        if _instance is None:
            _instance = EntityManager_2D()
        return _instance

    def clear(self):
        self._dynamic_entities.clear()
        self._entities.clear()
        self._batches.clear()
        self._remove_batch_list.clear()
        self._remove_batch_list.clear()

    def add_entity_list(self, _ents: List[Entity_2D]):
        for e in _ents:
            self.add_entity(e)

    def add_entity(self, _ent: Entity_2D):
        # Add static collider if no rigidbody is present
        ColliderManager_2D.get_singleton().add(_ent)

        self._entities[_ent.name] = _ent
        if _ent.rigidbody is not None:
            self._dynamic_entities[_ent.name] = _ent

    def add_batch(self, _batch: SpriteBatch):
        # Add static collider if no rigidbody is present
        _ent: Entity_2D
        for _ent in _batch.get_entities():
            ColliderManager_2D.get_singleton().add(_ent)

        self._batches[_batch.name] = _batch

    def remove_entity(self, _ent: Entity_2D):
        self._remove_entity_list.append(_ent)

    def remove_batch(self, _batch: SpriteBatch):
        self._remove_batch_list.append(_batch)

    def update(self, delta_time: float):
        # ENTITY
        e: Entity_2D
        for e in self._remove_entity_list:
            self._entities.pop(e.name, None)
        self._remove_entity_list.clear()

        for key, value in self._entities.items():
            if value.enabled is True:
                # General Update
                value.update(delta_time)
                # Update Collision with other dynamic entities
                if value.rigidbody is not None:
                    ColliderManager_2D.get_singleton().process_collision(
                        value,
                        self._dynamic_entities.values()
                    )
                    pass

        # BATCH
        b: SpriteBatch
        for b in self._remove_batch_list:
            self._batches.pop(b.name, None)
        self._remove_batch_list.clear()

    def draw(self):
        # Entity
        for key, value in self._entities.items():
            if value.enabled is True:
                value.draw()

        # Batches
        for key, value in self._batches.items():
            value.draw()
