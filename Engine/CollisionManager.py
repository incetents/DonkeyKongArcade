
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# System to manage locations of all colliders
from typing import Dict
from Engine.Vector import *
from Engine.Collision import *
from Engine.Entity import *
from Engine.Vector import *
import Engine.Graphics

CHUNK_SIZE = 64
CHUNK_SIZE_VEC_HALF = Vector2(CHUNK_SIZE/2, CHUNK_SIZE/2)
CHUNK_SIZE_VEC = Vector2(CHUNK_SIZE, CHUNK_SIZE)

_instance = None


class ColliderChunk:
    def __init__(self, _pos: Vector2):
        self.position: Vector2 = _pos
        self._colliders: Set[Collider] = set()

    def add_collider(self, collider: Collider):
        self._colliders.add(collider)

    def remove_collider(self, collider: Collider):
        if collider in self._colliders:
            self._colliders.remove(collider)

    def get_colliders(self) -> List[Collider]:
        return list(self._colliders)


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

    def get_chunks_from_square_region(self, pos: Vector2, size: Vector2):
        _chunks: List[ColliderChunk] = []

        return list(set(_chunks))
        pass

    def get_chunks_from_collider_aabb_2d(self, collider: Collider_AABB_2D):
        _chunks: List[ColliderChunk] = []
        _pos1 = Vector2(collider.get_left(), collider.get_down())
        _pos2 = Vector2(collider.get_left(), collider.get_up())
        _pos3 = Vector2(collider.get_right(), collider.get_down())
        _pos4 = Vector2(collider.get_right(), collider.get_up())
        _chunks.append(self.get_chunk(_pos1))
        _chunks.append(self.get_chunk(_pos2))
        _chunks.append(self.get_chunk(_pos3))
        _chunks.append(self.get_chunk(_pos4))
        # Return chunks with duplicates removed
        # print('size:', len(list(set(_chunks))))
        return list(set(_chunks))

    def get_chunk(self, pos: Vector2) -> ColliderChunk:
        _index_val = (pos / CHUNK_SIZE).__floor__()
        _index: Tuple[float,float] = (_index_val.x,_index_val.y)
        # Create Chunk if doesn't exist
        if _index not in self._chunks:
            print(
                'new chunk', _index
            )
            self._chunks[_index] = ColliderChunk(_index_val)
        return self._chunks[_index]

    def _add_collider(self, collider: Collider):
        _chunk = self.get_chunk(Vector2(collider.position.x, collider.position.y))
        _chunk.add_collider(collider)

    def add_static_collider(self, ent: Entity_2D):
        if ent.rigidbody is None:
            if type(ent.collision) is 'Collider_AABB_2D':
                pass
            elif type(ent.collision) is 'Collider_Circle_2D':
                pass
            else:
                print('unknown collider type attemped to be added')
        else:
            print('cannot add static collider if rigidbody is present')

    def draw_chunks(self):
        for i in self._chunks.values():
            Debug.draw_square_2d(
                (i.position * CHUNK_SIZE) + CHUNK_SIZE_VEC_HALF, CHUNK_SIZE_VEC, Vector3(0,0,0.5)
            )


    pass