
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Physics Movement]

from Engine.Vector import *
from typing import List
import math
from Engine.Collision import *
from Engine.Component import *


def clamp(_val, _min, _max):
    return max(_min, min(_max, _val))


class Rigidbody(Component):
    def __init__(self, position_ref: Vector3):
        super().__init__()
        self.enabled: bool = True
        self.ignore_static_colliders: bool = False
        self.ignore_dynamic_colliders: bool = False
        self._position: Vector3 = position_ref
        self._velocity: Vector3 = Vector3()
        self._gravity: Vector3 = Vector3()
        self._gravity_toggle: bool = True

        self._terminal_velocity: Vector3 = Vector3()
        self._terminal_velocity_switch: List[bool] = [False, False, False]

    # Increase
    def increase_position(self, increase: Vector3):
        self._position += increase

    def increase_velocity(self, increase: Vector3):
        self._velocity += increase

    # Setters
    def set_position(self, _position: Vector3):
        self._position = _position

    def set_velocity(self, _velocity: Vector3):
        self._velocity = _velocity

    def set_vel_x(self, _val: float):
        self._velocity.x = _val

    def set_vel_y(self, _val: float):
        self._velocity.y = _val

    def set_gravity(self, _gravity: Vector3):
        self._gravity = _gravity

    def set_gravity_state(self, _state: bool):
        self._gravity_toggle = _state

    def set_terminal_velocity_x(self, _val: float):
        self._terminal_velocity.x = _val
        self._terminal_velocity_switch[0] = True

    def set_terminal_velocity_y(self, _val: float):
        self._terminal_velocity.y = _val
        self._terminal_velocity_switch[1] = True

    def set_terminal_velocity_z(self, _val: float):
        self._terminal_velocity.z = _val
        self._terminal_velocity_switch[2] = True

    # Getters
    def get_position(self) -> Vector3:
        return self._position

    def get_velocity(self) -> Vector3:
        return self._velocity

    def get_gravity(self) -> Vector3:
        return self._gravity

    # Update
    def update(self, delta_time: float):
        if self.enabled is False:
            return

        # Increase Velocity from gravity
        if self._gravity_toggle is True:
            self._velocity += (self._gravity * delta_time)

        # Terminal Velocity Fix
        for i in range(3):
            if self._terminal_velocity_switch[i]:
                self._velocity[i] = clamp(
                    +self._velocity[i],
                    -self._terminal_velocity[i],
                    +self._terminal_velocity[i]
                )

        # Apply Velocity
        self._position += (self._velocity * delta_time)

