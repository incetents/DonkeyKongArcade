
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Managing Position / Rotation / Scale for objects

from Engine.Vector import *
from OpenGL.GL import *
from typing import List

class Transform:
    def __init__(self):
        self._parent = None
        self._position: Vector3 = Vector3()
        self._rotation_dir: Vector3 = Vector3(0, 0, 1)
        self._rotation_val: float = 0
        self._scale: Vector3 = Vector3(1, 1, 1)
        self._flip: List[bool] = [False, False, False]

    # Increasers
    def increase_position(self, position: Vector3):
        self._position += position

    def increase_rotation_amount(self, value: float):
        self._rotation_val += value

    def increase_scale(self, scale: Vector3):
        self._scale += scale

    # Setters
    def set_position(self, position: Vector3):
        # Must not change reference
        self._position.x = position.x
        self._position.y = position.y
        self._position.z = position.z

    def set_rotation_vector(self, rotation_dir: Vector3):
        self._rotation_dir = rotation_dir

    def set_rotation_amount(self, rotation_val: float):
        self._rotation_val = rotation_val

    def set_scale(self, scale: Vector3):
        self._scale = scale

    def set_parent(self, parent):
        self._parent = parent

    def set_flip_x(self, state: bool):
        self._flip[0] = state

    def set_flip_y(self, state: bool):
        self._flip[1] = state

    def set_flip_z(self, state: bool):
        self._flip[2] = state

    def set_flips(self, states: List[bool]):
        self._flip = states

    # Getters
    def get_position(self) -> Vector3:
        return self._position

    def get_scale(self) -> Vector3:
        return self._scale

    def get_rotation_amount(self) -> float:
        return self._rotation_val

    def get_flip_x(self) -> float:
        if self._flip[0] is False:
            return 1.0
        else:
            return -1.0

    def get_flip_y(self) -> float:
        if self._flip[1] is False:
            return 1.0
        else:
            return -1.0

    def get_flip_z(self) -> float:
        if self._flip[2] is False:
            return 1.0
        else:
            return -1.0

    def get_flips(self) -> List[bool]:
        return self._flip

    # Apply Transformation on current pipeline state
    def apply(self):
        glTranslatef(
            self._position.x,
            self._position.y,
            self._position.z
        )
        glScalef(
            self._scale.x * (-1 if self._flip[0] is True else +1),
            self._scale.y * (-1 if self._flip[1] is True else +1),
            self._scale.z * (-1 if self._flip[2] is True else +1)
        )
        glRotatef(
            self._rotation_val,
            self._rotation_dir.x, self._rotation_dir.y, self._rotation_dir.z
        )

