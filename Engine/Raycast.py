
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Find collision detection points

from Engine.Vector import *
from Engine.Collision import *
from Engine.CollisionManager import *
from typing import *
from Engine.Entity import *
import Engine.Collision

def Raypoint_2D(position: Vector2) -> List[Entity]:
    _result: List[Entity] = []
    _chunk = ColliderManager_2D.get_singleton().get_chunk(position)
    # inside the chunk get all entities that touch point
    _ents = _chunk.get_entities()
    for e in _ents:
        if e.collision.check_if_point_inside(position):
            _result.append(e)

    return _result


class Raycast_2D:
    def __init__(self, position: Vector2, direction: Vector2, distance: float=100, ignore_trigger: bool=True):
        self._position: Vector2 = position
        self._direction: Vector2 = direction.normalize()
        self._distance = distance
        self.ray_end: Vector2 = Vector2()
        self.hit_flag: bool = False
        self.hit_point: Vector2 = None
        self.hit_distance: float = -1

        # Create Square Region of Raycast
        self.ray_end: Vector2 = self._position + (self._direction * self._distance)
        _center: Vector2 = (self._position + self.ray_end) / 2
        _size = Vector2(abs(self._position.x - self.ray_end.x), abs(self._position.y - self.ray_end.y))
        # Get all chunks that are inside the square region

        _chunks = ColliderManager_2D.get_singleton().get_chunks_from_square_region_safe(_center, _size)
        # Check chunks that intersect with lines
        _chunks_intersect: List[ColliderChunk] = []
        for chunk in _chunks:
            if chunk._collider.check_if_line_inside(position, self.ray_end):
                _chunks_intersect.append(chunk)

        # print(len(_chunks_intersect))
        # Inside each chunk, get colliding point,
        for i in _chunks_intersect:
            _hit_flag = False
            ents = i.get_entities()
            # check all entities
            for e in ents:
                # Ignore potential
                if e.collision.type is Collision_Type.TRIGGER and ignore_trigger:
                    continue

                # if collision occurs, check intersection
                _mem: Tuple[Vector2, bool] = e.collision.get_hit_point(self._position, self._direction, self._distance)
                if _mem[1] is True:
                    # First collision is stored
                    if self.hit_point is None:
                        self.hit_point = _mem[0]
                        self.hit_flag = True
                    # Subsequent collisions only override hit value if they are closer to the start
                    else:
                        if (_mem[0] - self._position).magnitude() < (self.hit_point - self._position).magnitude():
                            self.hit_point = _mem[0]



        # Safety Check for hit in case nothing is hit
        if self.hit_point is None:
            self.hit_point = Vector2()
        # Update distance if a hit occurs
        else:
            self.hit_distance = (self.hit_point - self._position).magnitude()

