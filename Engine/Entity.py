
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Base Entity Class for appearance and movement

from __future__ import annotations
from Engine.Texture import Texture
from Engine.Graphics import Mesh
from Engine.Transform import Transform
from Engine.Sprite import Sprite
import Engine.Storage
# Physics
from Engine.Rigidbody import *
from Engine.Collision import *
import Engine.Collision

class Entity_2D:
    def __init__(self, ent_name: str):
        self.transform: Transform = Transform()
        self.rigidbody: Rigidbody = None
        self.collision: Collider = None
        # Add To Storage
        Engine.Storage.add(Engine.Storage.Type.ENTITY_2D, ent_name, self)

    def col_collider_stay(self, collider: Collider):
        pass

    def col_collider_enter(self, collider: Collider):
        pass

    def col_collider_exit(self, collider: Collider):
        pass

    def col_trigger_stay(self, trigger: Collider):
        pass

    def col_trigger_enter(self, trigger: Collider):
        pass

    def col_trigger_exit(self, trigger: Collider):
        pass

    def process_collision_start(self):
        # Requires collision box and rigidbody to process collision
        if self.collision is None or self.rigidbody is None:
            return

        # collision setup
        self.collision.clear_contact_collider()
        pass

    def process_collision_end(self):
        # Requires collision box and rigidbody to process collision
        if self.collision is None or self.rigidbody is None:
            return

        # Collision aftermath for exiting colliders
        _col_exit: List[Collider] = self.collision.get_exiting_colliders()
        for i in _col_exit:
            if i.type is Collision_Type.TRIGGER:
                self.col_trigger_exit(i)
            else:
                self.col_collider_exit(i)

    def process_collision_list(self, entities: List[Entity_2D]):
        # Requires collision box and rigidbody to process collision
        if self.collision is None or self.rigidbody is None:
            return

        # If either collision is disabled, stop this
        if self.collision.enabled is False:
            return

        # Rigidbody must be active
        if self.rigidbody.get_enabled() is False:
            return

        # Collision Simple
        for i in entities:
            # Ignore disabled colliders
            if i.collision.enabled is False:
                continue

            # Check Collide between both colliders
            if Engine.Collision.check2d(self.collision, i.collision) is True:
                # Add contact for reference
                _enter = self.collision.add_contact_collider(i.collision)

                # Check Collision Type
                if i.collision.type is Collision_Type.TRIGGER:
                    # Triggers only updates reference functions
                    if _enter:
                        self.col_trigger_enter(i.collision)
                    self.col_trigger_stay(i.collision)
                else:
                    # Collision moves rigidbody and updates functions
                    Engine.Collision.resolve2d(self.collision, i.collision, self.rigidbody)
                    if _enter:
                        self.col_collider_enter(i.collision)
                    self.col_collider_stay(i.collision)

    def process_collision(self, entity):
        _entities_one: List = [entity]
        self.process_collision_list(_entities_one)
        pass


class Entity_3D:
    def __init__(self, ent_name: str):
        self.transform: Transform = Transform()
        self._texture: Texture = None
        self._mesh: Mesh = None
        self._rigidbody: Rigidbody = None
        self._collision: Collider = None
        # Add To Storage
        Engine.Storage.add(Engine.Storage.Type.ENTITY_3D, ent_name, self)

    def set_texture(self, texture_name: str):
        self._texture = Engine.Storage.get(Engine.Storage.Type.TEXTURE, texture_name)

    def set_mesh(self, mesh_name: str):
        self._mesh = Engine.Storage.get(Engine.Storage.Type.MESH, mesh_name)

    def draw(self):
        # Bind Texture and Draw Mesh
        if (self._texture is not None) and (self._mesh is not None):
            self._texture.bind()
            self._mesh.draw(self.transform)

