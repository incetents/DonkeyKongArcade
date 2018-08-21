
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Trigger Zones that are static or follow rigidbodies

from __future__ import annotations
from Engine.Entity import *
from Engine.EntityManager import *
import pygame
# Physics
from Engine.Rigidbody import *
from Engine.Collision import *


class TriggerZone(Entity):
    def __init__(self, ent_name: str, ent_follow: Entity,
                 col_id: int,
                 col_size: Vector2 = Vector2(), col_offset: Vector2 = Vector2()
                 ):
        # Base
        Entity.__init__(self, ent_name)
        # ent reference
        self._entity = ent_follow
        if self._entity is not None:
            self.transform.set_position(self._entity.transform.get_position())
        # Physics
        self.rigidbody: Rigidbody = self.add_component(Rigidbody(self.transform.get_position()))
        self.rigidbody.ignore_dynamic_colliders = True
        self.rigidbody.ignore_static_colliders = True

        self.collision: Collider_AABB_2D = self.add_component(Collider_AABB_2D(self.transform.get_position()))
        self.collision.size = col_size
        self.collision.offset = col_offset
        self.collision.type = Collision_Type.TRIGGER
        self.collision.id = col_id

    def update(self, delta_time):
        if self._entity is None:
            return

        if self._entity.deleted:
            EntityManager.get_singleton().remove_entity(self)
        else:
            self.rigidbody.update(delta_time)
            self.transform.set_position(self._entity.transform.get_position())
        pass

    def draw(self):
        pass

    def draw_debug(self):
        self.collision.draw(Vector3(0, 1, 0.5))

        Debug.draw_line_2d(
            self.collision.get_position().get_vec2() + Vector2(-8, -2),
            self.collision.get_position().get_vec2() + Vector2(+8, -2),
            Vector3(0.75, 0.75, 0)
        )










