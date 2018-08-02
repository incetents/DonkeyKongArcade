
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Tiles for Mario, Enemies and Barrels to displace themselves on]

# Entity
from Engine.Entity import *
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
        # Add to collision manager
        ColliderManager_2D.get_singleton().add_static_collider(self)

    def update(self, delta_time):
        pass

    def draw(self):
        self.sprite.draw(self.transform)
        self.collision.draw(Vector3(1,0,0))


class GameTiles(Entity_2D):
    def __init__(self, entity_name: str, floor_sprname: str, ladder_sprname: str):
        # Base Constructor
        Entity_2D.__init__(self, entity_name)

        self._tiles: List[Tile] = []

        self._floor_spr: str = floor_sprname
        self._ladder_spr: str = ladder_sprname

        self._floorBatch: SpriteBatch = SpriteBatch(floor_sprname)
        self._ladderBatch: SpriteBatch = SpriteBatch(ladder_sprname)

        self.add_pos_offset: Vector3 = Vector3()

    def clear(self):
        self._tiles.clear()
        self._floorBatch.clear()
        self._ladderBatch.clear()

    def add_tile_floor(self, _position: Vector3):
        # Add Tile
        _tile = Tile('tile' + str(len(self._tiles)+1), self._floor_spr, _position + self.add_pos_offset)
        _tile.collision.type = Collision_Type.PLATFORM
        self._tiles.append(_tile)
        # Add to batch
        self._floorBatch.add_model(_tile.transform)

    def add_tile_ladder(self, _position: Vector3):
        # Add Tile
        _tile = Tile('tile' + str(len(self._tiles)+1), self._ladder_spr, _position + self.add_pos_offset)
        _tile.collision.type = Collision_Type.TRIGGER
        _tile.collision.id = Engine.Config.TRIGGER_ID_LADDER
        self._tiles.append(_tile)
        # Add to batch
        self._ladderBatch.add_model(_tile.transform)

    def update(self, delta_time):
        for i in self._tiles:
            # Update Normally
            i.update(delta_time)
            # Collision
            pass

    def draw(self):
        pass
        # Draw Batch
        self._floorBatch.draw()
        self._ladderBatch.draw()