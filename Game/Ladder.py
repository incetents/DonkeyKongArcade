
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Ladders for barrels and mario to displace vertically]

# Entity
from Engine.Entity import *
from Engine.EntityManager import *
# Math
from Engine.Vector import *
# Physics
from Engine.Collision import *
import Engine.Collision
from Engine.CollisionManager import *
# Misc
import Engine.Config

class Ladder(Entity):
    def __init__(self, entity_name: str, sprite_name: str, new_position: Vector3):
        # Base Constructor
        Entity.__init__(self, entity_name)
        self.sprite: Sprite = Engine.Storage.get(Engine.Storage.Type.SPRITE, sprite_name)
        # Default Transform
        self.transform.set_position(new_position)
        # Collision
        self.collision = self.add_component(Collider_AABB_2D(self.transform.get_position()))
        self.collision.set_size_from_sprite(self.transform, self.sprite)
        self.collision.offset = self.sprite.get_scale_half()
        self.collision.type = Collision_Type.TRIGGER
        self.collision.id = Engine.Config.TRIGGER_ID_LADDER

    def update(self, delta_time):
        pass

    def draw(self):
        self.sprite.draw(self.transform)
        self.collision.draw(Vector3(1, 0, 0))