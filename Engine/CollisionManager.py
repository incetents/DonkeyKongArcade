
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# System to manage locations of all colliders
from __future__ import annotations
from typing import Dict
from Engine.Vector import *
from Engine.Collision import *
from Engine.Entity import *
from Engine.Vector import *
import Engine.Graphics
from Engine.Collision import *

CHUNK_SIZE = 32
CHUNK_SIZE_VEC_HALF = Vector2(CHUNK_SIZE/2, CHUNK_SIZE/2)
CHUNK_SIZE_VEC = Vector2(CHUNK_SIZE, CHUNK_SIZE)

_instance = None


class ColliderChunk:
    def __init__(self, _pos: Vector3):
        self.position: Vector3 = _pos
        self._collider = Collider_AABB_2D(self.position, Vector3(CHUNK_SIZE,CHUNK_SIZE,1))
        self._collider.offset = CHUNK_SIZE_VEC_HALF
        self._ref_entities_2d: Set[Entity] = set()

    def get_id_position(self) -> Vector2:
        return self.position.get_vec2() / CHUNK_SIZE

    def add_entity(self, entity: Entity):
        self._ref_entities_2d.add(entity)

    def remove_entity(self, entity: Entity):
        if entity in self._ref_entities_2d:
            self._ref_entities_2d.remove(entity)

    def get_entities(self) -> List[Entity]:
        return list(self._ref_entities_2d)


class ColliderManager_2D:
    def __init__(self):
        self._chunks: Dict[Tuple[float, float], ColliderChunk] = {}

    @staticmethod
    def get_singleton():
        global _instance
        if _instance is None:
            _instance = ColliderManager_2D()
        return _instance

    def clear(self):
        self._chunks.clear()

    def get_chunks_from_square_region_unsafe(self, pos: Vector2, size: Vector2):
        _chunks: Set[ColliderChunk] = set()
        _chunks.add(self.get_chunk(pos + Vector2(-size.x * 0.5, -size.y * 0.5)))
        _chunks.add(self.get_chunk(pos + Vector2(+size.x * 0.5, -size.y * 0.5)))
        _chunks.add(self.get_chunk(pos + Vector2(+size.x * 0.5, +size.y * 0.5)))
        _chunks.add(self.get_chunk(pos + Vector2(-size.x * 0.5, +size.y * 0.5)))
        return list(_chunks)

    def get_chunks_from_square_region_safe(self, pos: Vector2, size: Vector2):
        _chunks: Set[ColliderChunk] = set()
        # Edges
        _left = pos.x - size.x * 0.5
        _right = pos.x + size.x * 0.5
        _top = pos.y + size.y * 0.5
        _bot = pos.y - size.y * 0.5
        # Acquire all possible chunks in the range
        _x = _left
        _y = _bot
        _final_row_offset: int = 2
        while _y <= _top or _final_row_offset > 0:
            while _x <= _right:
                _chunks.add(self.get_chunk(Vector2(_x, _y)))
                _x = min(_x + CHUNK_SIZE, _right + 0.01)
                # Edge case (ignored if left and right are the same)
                if (_right - _x) < 0.01 and (_right - _left) > 0.01:
                    _chunks.add(self.get_chunk(Vector2(_right + 1, _y)))

            _y = min(_y + CHUNK_SIZE, _top + 0.01)
            _x = _left

            # Edge case (ignored if top and bottom are the same)
            if (_top - _bot) < 0.01:
                _final_row_offset = 0
                break
            elif (_top - _y) < 0.01:
                _final_row_offset -= 1

        return list(_chunks)

    def get_chunks_from_collider_aabb_2d(self, collider: Collider_AABB_2D):
        if collider.size.x > CHUNK_SIZE or collider.size.y > CHUNK_SIZE:
            return self.get_chunks_from_square_region_safe(collider.get_position().get_vec2(), collider.size)
        else:
            return self.get_chunks_from_square_region_unsafe(collider.get_position().get_vec2(), collider.size)

    def get_chunks_from_collider(self, collider):
        if type(collider) is Collider_AABB_2D:
            return self.get_chunks_from_collider_aabb_2d(collider)
        else:
            print('process collision error 101')

    def get_chunk(self, world_pos: Vector2) -> ColliderChunk:
        _index_val = (world_pos / CHUNK_SIZE).__floor__()
        _index: Tuple[float,float] = (_index_val.x, _index_val.y)
        # Create Chunk if doesn't exist
        if _index not in self._chunks:
            # print('new chunk', _index)
            self._chunks[_index] = ColliderChunk(Vector3(_index_val.x, _index_val.y, 0) * CHUNK_SIZE)
        return self._chunks[_index]

    def process_collision(self, _entity: Entity, _others: List[Entity] = []):
        _chunks = self.get_chunks_from_collider(_entity.collision)

        # Begin
        _entity.process_collision_start()

        # Create list of all possible entities in region
        _megalist: List[Entity] = []
        for c in _chunks:
            _megalist += c.get_entities()

        _megalist += _others

        # Process all those entities
        # print('ent:', _entity.name, ' checking: ', len(_megalist))
        _entity.process_collision_list(_megalist)

        # End
        _entity.process_collision_end()

    def add(self, ent: Entity):

        # Static Collider
        if ent.rigidbody is None:
            # Add Collider based on type
            if type(ent.collision) is Collider_AABB_2D:
                _col: Collider_AABB_2D = ent.collision
                _chunks = self.get_chunks_from_collider_aabb_2d(_col)
                for i in _chunks:
                    i.add_entity(ent)

            elif type(ent.collision) is Collider_Circle_2D:
                _col: Collider_Circle_2D = ent.collision
                _chunks = self.get_chunks_from_square_region_unsafe(
                    _col.get_position().get_vec2(),
                    Vector2(_col.radius * 2.0, _col.radius * 2.0)
                )
                for i in _chunks:
                    i.add_entity(ent)

            else:
                print('unknown collider type attemped to be added:', ent.collision)

    def draw_chunks(self):
        for i in self._chunks.values():
            Debug.draw_square_2d(
                i._collider.get_position(), CHUNK_SIZE_VEC, Vector3(0, 0, 0.5)
            )
