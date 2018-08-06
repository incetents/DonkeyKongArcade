
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
from Engine.Component import *


class Entity:
    def __init__(self, ent_name: str):
        self.name: str = ent_name
        # Special Case
        self.deleted: bool = False
        self.enabled: bool = True

        # Components
        self._components: Dict(type, Component) = {}
        # Transform (always present in entities)
        self.transform: Transform = Transform()
        self.add_component(self.transform)

        # Add To Storage
        Engine.Storage.add(Engine.Storage.Type.Entity, ent_name, self)

    def update(self, delta_time):
        pass

    def draw(self):
        pass

    def add_component(self, component: Component):
        # cannot be base class
        if type(component) is not Component:
            self._components[type(component)] = component
        else:
            print('attempting to add duplicate components', component, ' on entity', self)
        return component

    def remove_component(self, component: Component):
        self._components.pop(type(component), None)

    def remove_all_components(self):
        self._components.clear()

    def get_component(self, component_type):
        if component_type in self._components:
            return self._components[component_type]

        return None

    def collider_stay(self, collider: Collider):
        pass

    def collider_enter(self, collider: Collider):
        pass

    def collider_exit(self, collider: Collider):
        pass

    def trigger_stay(self, trigger: Collider):
        pass

    def trigger_enter(self, trigger: Collider):
        pass

    def trigger_exit(self, trigger: Collider):
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
                self.trigger_exit(i)
            else:
                self.collider_exit(i)

    def process_collision_list(self, entities: List[Entity]):
        # Collision and rigidbody must be present
        if self.collision is None or self.rigidbody is None:
            return

        # Both collision and rigidbody must be active
        if self.collision.enabled is False or self.rigidbody.enabled is False:
            return

        # Collision Simple
        for i in entities:

            # Ignore self
            if i is self:
                continue

            # Ignore disabled colliders
            if (i.enabled is False) or (i.collision.enabled is False):
                continue

            # Check Collide between both colliders
            if Engine.Collision.check2d(self.collision, i.collision) is True:
                # Add contact for reference
                _enter = self.collision.add_contact_collider(i.collision)

                # Check Collision Type
                if i.collision.type is Collision_Type.TRIGGER:
                    # Triggers only updates reference functions
                    if _enter:
                        self.trigger_enter(i.collision)
                    self.trigger_stay(i.collision)
                else:
                    # Collision moves rigidbody and updates functions
                    Engine.Collision.resolve2d(self.collision, i.collision, self.rigidbody)
                    if _enter:
                        self.collider_enter(i.collision)
                    self.collider_stay(i.collision)

    def process_collision(self, entity):
        _entities_one: List = [entity]
        self.process_collision_list(_entities_one)
        pass

