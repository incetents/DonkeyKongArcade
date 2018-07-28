
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Find collision detection points

from Engine.Vector import *
from Engine.Collision import *
from Engine.CollisionManager import *
from typing import *

class Raycast_2D:
#
    def __init__(self, position: Vector2, direction: Vector2, distance: float=100):
        self._position: Vector2 = position
        self._direction: Vector2 = direction.normalize()
        self._distance = distance
        self.hit: Vector2 = None
        self.hit_flag: bool = False

        # Create Square Region of Raycast
        _p2: Vector2 = self._position + (self._direction * self._distance)
        _center: Vector2 = (self._position + _p2) / 2
        _size = Vector2(abs(self._position.x - _p2.x), abs(self._position.y - _p2.y))
        # Get all chunks that are inside the square region

        _chunks = ColliderManager_2D.get_singleton().get_chunks_from_square_region(_center, _size)
        # Check chunks that intersect with lines
        _chunks_intersect: List[ColliderChunk] = []
        for chunk in _chunks:
            if chunk._collider.check_if_line_inside(position, _p2):
                _chunks_intersect.append(chunk)

        # print(len(_chunks_intersect))
        # Inside each chunk, get colliding point,
        for i in _chunks_intersect:
            _hit_flag = False
            ents = i.get_entities()
            # check all entities
            for e in ents:
                # if collision occurs, check intersection
                _mem: Tuple[Vector2, bool] = e.collision.get_hit_point(self._position, self._direction, self._distance)
                if _mem[1] is True:
                    # First collision is stored
                    if self.hit is None:
                        self.hit = _mem[0]
                        self.hit_flag = True
                    # Subsequent collisions only override hit value if they are closer to the start
                    else:
                        if (_mem[0] - self._position).magnitude() < (self.hit - self._position).magnitude():
                            self.hit = _mem[0]




        # Safety Check for hit in case nothing is hit
        if self.hit is None:
            self.hit = Vector2()

        pass

