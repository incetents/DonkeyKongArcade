
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Find collision detection points

from Engine.Vector import *
from Engine.Collision import *
from Engine.CollisionManager import *

class Raycast_2D:
    def __init__(self, position: Vector2, direction: Vector2, distance: float=100):
        self._position: Vector2 = position
        self._direction: Vector2 = direction.normalize()
        self._distance = distance
        # Create Square Region of Raycast
        _p2: Vector2 = self._position + (self._direction * self._distance)
        _center: Vector2 = (self._position + _p2) / 2
        _size = Vector2(abs(self._position.x - _p2.x), abs(self._position.y - _p2.y))
        _chunks = ColliderManager_2D.get_singleton().get_chunks_from_square_region(_center, _size)
        print('~~~~')
        for i in _chunks:
            print(i)
        pass

