
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


class Tile(Entity):
    def __init__(self, entity_name: str, sprite_name: str, new_position: Vector3):
        # Base Constructor
        Entity.__init__(self, entity_name)
        self.sprite: Sprite = self.add_component(Engine.Storage.get(Engine.Storage.Type.SPRITE, sprite_name))
        # Default Transform
        self.transform.set_position(new_position)
        # Collision
        self.collision = self.add_component(Collider_AABB_2D(self.transform.get_position()))
        self.collision.set_size_from_sprite(self.transform, self.sprite)

    def update(self, delta_time):
        pass

    def draw(self):
        self.sprite.draw(self.transform)
        self.collision.draw(Vector3(1,0,0))


class TileBatch(SpriteBatch):
    def __init__(self, batch_name: str, texture_name: str, collision_type: Collision_Type, collision_id: int=0):
        super().__init__(batch_name, texture_name)
        self._collision_type: Collision_Type = collision_type
        self._collision_id: int = collision_id

    def add_tile(self, _position: Vector3, _sprite_name: str):
        # Create Tile
        _tile = Tile('tile' + str(self.get_size()), _sprite_name, _position)
        _tile.collision.type = self._collision_type
        _tile.collision.id = self._collision_id

        _tile.collision.offset = Vector2(_tile.sprite.get_scale().x / 2, _tile.sprite.get_scale().y / 2)
        # Add to batch
        self.add_entity(_tile)
