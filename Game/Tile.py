
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Tiles for Mario, Enemies and Barrels that are simply static]

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
from typing import List
from Engine.Sprite import *
from Engine.SpriteBatch import *
import Engine.Storage
import Engine.Config


class Tile(Entity_2D):
    def __init__(self, entity_name: str, sprite_name: str, new_position: Vector3):
        # Base Constructor
        Entity_2D.__init__(self, entity_name)
        self.sprite = Engine.Storage.get(Engine.Storage.Type.SPRITE, sprite_name)
        # Default Transform
        self.transform.set_position(new_position)
        # Collision
        self.collision = Collider_AABB_2D(self.transform.get_position())
        self.collision.set_size_from_sprite(self.transform, self.sprite)
        self.collision.offset = Vector2(4, 4)

    def update(self, delta_time):
        pass

    def draw(self):
        self.sprite.draw(self.transform)
        self.collision.draw(Vector3(1,0,0))


class TileBatch(SpriteBatch):
    def __init__(self, batch_name: str, sprite_name: str, collision_type: Collision_Type, collision_id: int=0):
        super().__init__(batch_name, sprite_name)
        self._collision_type: Collision_Type = collision_type
        self._collision_id: int = collision_id

    def add_tile(self, _position: Vector3):
        # Create Tile
        _tile = Tile('tile' + str(self.get_size()), self.get_sprite().get_name(), _position)
        _tile.collision.type = self._collision_type
        _tile.collision.id = self._collision_id
        # Add to batch
        self.add_entity(_tile)
