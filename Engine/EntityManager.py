
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# System for organizing, updating and drawing all entities for a scene
from typing import *
from Engine.Entity import *
from Engine.SpriteBatch import *
from Engine.CollisionManager import *
import Engine.CollisionManager
from collections import OrderedDict
import multiprocessing

_instance = None


class EntityManager:
    def __init__(self):
        self._dynamic_entities: Dict[str, Entity] = {}
        self._entities: Dict[str, Entity] = {}
        self._entities_ordered: OrderedDict[int, List[Entity]] = OrderedDict()
        self._remove_entity_list: List[Entity] = []

        self._batches: Dict[str, SpriteBatch] = {}
        self._remove_batch_list: List[SpriteBatch] = []

    @staticmethod
    def get_singleton():
        global _instance
        if _instance is None:
            _instance = EntityManager()
        return _instance

    def clear(self):
        self._dynamic_entities.clear()
        self._entities.clear()
        self._entities_ordered.clear()
        self._batches.clear()
        self._remove_batch_list.clear()
        self._remove_batch_list.clear()

    def get_entity(self, name: str):
        if name in self._entities.keys():
            return self._entities[name]

    def add_entity_list(self, _entities: List[Entity]):
        for e in _entities:
            self.add_entity(e)

    def check_entity(self, _ent: Entity):
        if _ent.name in self._entities:
            return True
        return False

    def add_entity(self, _ent: Entity):
        if _ent is None:
            return

        # Add static collider if no rigidbody is present
        ColliderManager_2D.get_singleton().add(_ent)

        # Add to list of all entities
        self._entities[_ent.name] = _ent

        # Add to list of ordered entities
        _depth: int = _ent.get_layer()

        if _depth not in self._entities_ordered:
            # Create empty slot
            self._entities_ordered[_depth] = []
            # Add entity to sorted list
            self._entities_ordered[_depth].append(_ent)
            # Sort Dictionary
            self._entities_ordered = OrderedDict(sorted(self._entities_ordered.items(), key=lambda t: t[0]))
        else:
            # Add entity to sorted list
            self._entities_ordered[_depth].append(_ent)

        # Add to dynamic entities
        if _ent.get_component(Rigidbody) is not None:
            self._dynamic_entities[_ent.name] = _ent
            # Create thread for entity
            # _thread = ProcessCollisionThread(_ent, self._dynamic_entities)
            # _thread.start()

    def add_batch(self, _batch: SpriteBatch):
        # Add static collider if no rigidbody is present
        _ent: Entity
        for _ent in _batch.get_entities():
            ColliderManager_2D.get_singleton().add(_ent)

        self._batches[_batch.name] = _batch

    def remove_entity(self, _ent: Entity):
        # ENTITY deletion flag
        _ent.deleted = True
        # Check for entity existence and delete it from any of the following containers
        if _ent in self._entities.values():
            self._entities.pop(_ent.name, None)

        _ordered_list: List[Entity] = self._entities_ordered[_ent.get_layer()]
        if _ent in _ordered_list:
            self._entities_ordered[_ent.get_layer()].remove(_ent)

        if _ent.get_component(Rigidbody) is not None and _ent in self._dynamic_entities.values():
            self._dynamic_entities.pop(_ent.name, None)

    def remove_batch(self, _batch: SpriteBatch):
        # BATCH deletion
        self._batches.pop(_batch.name, None)

    def update(self, delta_time: float):
        # ENTITY update
        # print('~~~')
        # _t = pygame.time.get_ticks()
        _ent_copy = self._entities.copy()
        for key, value in _ent_copy.items():
            if value.enabled is True:
                # General Update
                value.update(delta_time)
                # Update Collision with other dynamic entities
                _rigid: Rigidbody = value.get_component(Rigidbody)
                if _rigid is not None and _rigid.enabled:
                    # print('mario rigid', self._dynamic_entities.values())
                    ColliderManager_2D.get_singleton().process_collision(
                        value,
                        self._dynamic_entities.values()
                    )
        # print('time for updating all ents:', pygame.time.get_ticks() - _t)

    def draw(self):
        # Batch Draw
        for key, value in self._batches.items():
            value.draw()

        # Unordered
        # for key, value in self._entities.items():
        #    if value.enabled is True:
        #        value.draw()

        # Ordered
        # Entity Draw (draw from ordered entity list)
        for key, value in self._entities_ordered.items():
            ent: Entity
            for ent in value:
                if ent.enabled is True:
                    ent.draw()

    def draw_debug(self):
        # Draw Debug of batches
        for value in self._batches.values():
            value.draw_debug()

        # Draw Debug of entities
        for value in self._entities.values():
            value.draw_debug()

