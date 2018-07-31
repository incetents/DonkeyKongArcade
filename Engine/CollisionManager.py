
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# System to manage locations of all colliders
from typing import Dict
from Engine.Vector import *
from Engine.Collision import *
from Engine.Entity import *
from Engine.Vector import *
import Engine.Graphics
from Engine.Collision import *
from Engine.Entity import *

CHUNK_SIZE = 64
CHUNK_SIZE_VEC_HALF = Vector2(CHUNK_SIZE/2, CHUNK_SIZE/2)
CHUNK_SIZE_VEC = Vector2(CHUNK_SIZE, CHUNK_SIZE)

_instance = None


class ColliderChunk:
    def __init__(self, _pos: Vector3):
        self.position: Vector3 = _pos
        self._collider = Collider_AABB_2D(self.position, Vector3(CHUNK_SIZE,CHUNK_SIZE,1))
        self._collider.offset = CHUNK_SIZE_VEC_HALF
        self._ref_entities_2d: Set[Entity_2D] = set()

    def get_id_position(self) -> Vector2:
        return self.position.get_vec2() / CHUNK_SIZE

    def add_entity(self, entity: Entity_2D):
        self._ref_entities_2d.add(entity)

    def remove_entity(self, entity: Entity_2D):
        if entity in self._ref_entities_2d:
            self._ref_entities_2d.remove(entity)

    def get_entities(self) -> List[Entity_2D]:
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


    def process_collision_aabb(self, _entity: Entity_2D, *_other: Entity_2D):
        _chunks = self.get_chunks_from_collider_aabb_2d(_entity.collision)

        _entity.process_collision_start()

        for c in _chunks:
            _entity.process_collision_list(c.get_entities())

        _entity.process_collision_list(list(_other))

        _entity.process_collision_end()
        pass

    def get_chunks_from_square_region(self, pos: Vector2, size: Vector2):
        _chunks: List[ColliderChunk] = []
        # Minimum Size of size vector for safety
        size.x = max(size.x, 1.0)
        size.y = max(size.y, 1.0)
        # Edges
        _left = pos.x - size.x * 0.5
        _right = pos.x + size.x * 0.5
        _top = pos.y + size.y * 0.5
        _bot = pos.y - size.y * 0.5
        # Acquire all possible chunks in the range
        _x = _left
        _y = _bot
        _final_row_offset: int = 2
        while _y < _top or _final_row_offset > 0:
            while _x < _right:
                _chunks.append(self.get_chunk(Vector2(_x, _y)))
                _x = min(_x + CHUNK_SIZE, _right)
                # Edge case
                if (_right - _x) < 0.01:
                    _chunks.append(self.get_chunk(Vector2(_right + 1, _y)))

            _y = min(_y + CHUNK_SIZE, _top)
            _x = _left

            # Edge case
            if (_top - _y) < 0.01:
                _final_row_offset -= 1

        return list(set(_chunks))

    def get_chunks_from_collider_aabb_2d(self, collider: Collider_AABB_2D):
        return self.get_chunks_from_square_region(collider.get_position().get_vec2(), collider.size)

    def get_chunk(self, world_pos: Vector2) -> ColliderChunk:
        _index_val = (world_pos / CHUNK_SIZE).__floor__()
        _index: Tuple[float,float] = (_index_val.x, _index_val.y)
        # Create Chunk if doesn't exist
        if _index not in self._chunks:
            # print('new chunk', _index)
            self._chunks[_index] = ColliderChunk(Vector3(_index_val.x, _index_val.y, 0) * CHUNK_SIZE)
        return self._chunks[_index]

    def add_static_collider(self, ent: Entity_2D):
        if ent.rigidbody is None:
            # Add Collider based on type

            if type(ent.collision) is Collider_AABB_2D:
                _col: Collider_AABB_2D = ent.collision
                _chunks = self.get_chunks_from_collider_aabb_2d(_col)
                for i in _chunks:
                    i.add_entity(ent)

            elif type(ent.collision) is Collider_Circle_2D:
                _col: Collider_Circle_2D = ent.collision
                _chunks = self.get_chunks_from_square_region(
                    _col.get_position().get_vec2(),
                    Vector2(_col.radius * 2.0, _col.radius * 2.0)
                )
                for i in _chunks:
                    i.add_entity(ent)

            else:
                print('unknown collider type attemped to be added:', ent.collision)
        else:
            print('cannot add static collider if rigidbody is present:', ent)

    def draw_chunks(self):
        for i in self._chunks.values():
            Debug.draw_square_2d(
                i._collider.get_position(), CHUNK_SIZE_VEC, Vector3(0,0,0.5)
            )


    pass