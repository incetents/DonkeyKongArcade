
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Colliders]

import math
from functools import singledispatch
from typing import *
from enum import Enum
from Engine.Vector import Vector2, Vector3
from Engine.Graphics import Debug
from Engine.Rigidbody import Rigidbody
from Engine.Transform import *
from Engine.Sprite import *

# 1D Collision General Use
#
def collision_1D_safe(line1_p1: float, line1_p2: float, line2_p1: float, line2_p2: float) -> bool:
    # Check intersection
    return line1_p2 >= line2_p1 and line2_p2 >= line1_p1


def collision_1D_unsafe(line1_p1: float, line1_p2: float, line2_p1: float, line2_p2: float) -> bool:
    # Check End points of lines
    _min_line1 = min(line1_p1, line1_p2)
    _max_line1 = max(line1_p1, line1_p2)
    _min_line2 = min(line2_p1, line2_p2)
    _max_line2 = max(line2_p1, line2_p2)
    # Check intersection
    return collision_1D_safe(_min_line1, _max_line1, _min_line2, _max_line2)


# Collision Checking Classes
#
class Collision_Type(Enum):
    SOLID = 1,
    TRIGGER = 2,
    PLATFORM = 3,


class Collider:
    def __init__(self, position: Vector3):
        self.position: Vector3 = position
        self.enabled: bool = True
        self.id: int = 0
        self.contact_list_prev: Set[Collider] = set()
        self.contact_list: Set[Collider] = set()
        pass

    def draw(self):
        pass

    # Special Functions used for COLLISION
    # --------------------------------------------

    # Clear current list of colliders and have prev list hold a backup copy
    def clear_contact_collider(self):
        self.contact_list_prev = self.contact_list.copy()
        self.contact_list.clear()
        # print(len(self.contact_list_prev))

    # Return true if entering collision, return false if already entered collision
    def add_contact_collider(self, collider) -> bool:
        if collider not in self.contact_list:
            self.contact_list.add(collider)
            # Check if not in prev list
            if collider not in self.contact_list_prev:
                return True
            else:
                return False

    # Check colliders that are being exited out of
    def get_exiting_colliders(self):
        _colliders = []
        # Any key present in prev but not in present is going to the list
        for key in self.contact_list_prev:
            if key not in self.contact_list:
                _colliders.append(key)

        return _colliders


class Collider_Circle_2D(Collider):
    def __init__(self, pos: Vector3=Vector3(), radius: float=1):
        Collider.__init__(self, pos)
        self.radius: float = radius

    def draw(self, _color: Vector3 = Vector3(0, 1, 0), _vertices:int = 40):
        Debug.draw_circle_2d(self.position, self.radius, _color, _vertices)


class Collider_AABB_2D(Collider):
    def __init__(self, pos: Vector3, size: Vector3=Vector3()):
        Collider.__init__(self, pos)
        self.size: Vector2 = size
        self.type: Collision_Type = Collision_Type.SOLID

    def update_size_from_sprite(self, model: Transform, spr: Sprite):
        self.size = Vector2(
            model.get_scale().x * spr.get_width(),
            model.get_scale().y * spr.get_height()
        )

    def get_left(self) -> float:
        return self.position.x - self.size.x * 0.5

    def get_right(self) -> float:
        return self.position.x + self.size.x * 0.5

    def get_up(self) -> float:
        return self.position.y + self.size.y * 0.5

    def get_down(self) -> float:
        return self.position.y - self.size.y * 0.5

    def draw(self, _color: Vector3 = Vector3(0, 1, 0)):
        Debug.draw_square_2d(self.position, self.size, _color)



# Collision Checking Functions
#
def check2d(collider1, collider2) -> bool:
    # Interpret correct collision

    # Both AABB
    if (type(collider1) is Collider_AABB_2D) and (type(collider2) is Collider_AABB_2D):
        return _check2d_aabb_aabb(collider1, collider2)

    # Both Circles
    elif (type(collider1) is Collider_Circle_2D) and (type(collider2) is Collider_Circle_2D):
        return _check2d_circle_circle(collider1, collider2)

    # Unknown collider combination
    else:
        print("Check2d cannot distinguish collider types: " + type(collider1) + ' and ' + type(collider2))
        return False


def _check2d_aabb_aabb(a1: Collider_AABB_2D, a2: Collider_AABB_2D) -> bool:
    _x_intersection = collision_1D_safe(a1.get_left(), a1.get_right(), a2.get_left(), a2.get_right())
    _y_intersection = collision_1D_safe(a1.get_down(), a1.get_up(), a2.get_down(), a2.get_up())
    return _x_intersection and _y_intersection


def _check2d_circle_circle(c1: Collider_Circle_2D, c2: Collider_Circle_2D) -> bool:
    _radius_total = c1.radius + c2.radius
    _distance = (c1.position - c2.position).magnitude()
    return _distance <= _radius_total


# Collision Resolving Functions
#
def resolve2d(collider1, collider2, rigid1: Rigidbody, rigid2: Rigidbody=None):
    # Interpret correct collision

    # Both AABB
    if (type(collider1) is Collider_AABB_2D) and (type(collider2) is Collider_AABB_2D):
        return _resolve2d_aabb_aabb(collider1, collider2, rigid1, rigid2)

    # Both Circles
    elif (type(collider1) is Collider_Circle_2D) and (type(collider2) is Collider_Circle_2D):
        return _resolve2d_circle_circle(collider1, collider2, rigid1, rigid2)

    # Unknown collider combination
    else:
        print("Check2d cannot distinguish collider types: " + type(collider1) + ' and ' + type(collider2))
        return False


def _resolve2d_aabb_aabb(a1: Collider_AABB_2D, a2: Collider_AABB_2D, rigid1: Rigidbody, rigid2: Rigidbody):
    # Error
    if rigid1 is None and rigid2 is None:
        return

    # Make sure both colliders and rigidbodies have same positions
    a1.position = rigid1.get_position()

    # Fix only first collider
    if rigid2 is None:

        # Platform Collision
        if a2.type is Collision_Type.PLATFORM:
            if a1.get_down() >= a2.position.y and rigid1.get_velocity().y <= 0:
                a1.position.y += a2.get_up() - a1.get_down()
                rigid1.set_vel_y(0)
            pass

        # Normal Collision
        elif a2.type is Collision_Type.SOLID:
            # Check depth of X and Y intersection
            _xdepth: int = 0
            _ydepth: int = 0
            _left: bool
            _up: bool

            # Check X position
            if a1.position.x < a2.position.x:
                # Depth
                _left = True
                _xdepth = a1.get_right() - a2.get_left()
            else:
                # Depth
                _left = False
                _xdepth = a2.get_right() - a1.get_left()

            # Check Y position
            if a1.position.y < a2.position.y:
                # Depth
                _up = False
                _ydepth = a1.get_up() - a2.get_down()
            else:
                # Depth
                _up = True
                _ydepth = a2.get_up() - a1.get_down()

            # Fix X-axis
            if _xdepth < _ydepth:
                if _left and rigid1.get_velocity().x > 0:
                    a1.position.x -= _xdepth
                elif not _left and rigid1.get_velocity().x < 0:
                    a1.position.x += _xdepth
                rigid1.set_vel_x(0)
            # Fix Y-axis
            else:
                if _up and rigid1.get_velocity().y < 0:
                    a1.position.y += _ydepth
                elif not _up and rigid1.get_velocity().y > 0:
                    a1.position.y -= _ydepth
                rigid1.set_vel_y(0)

            # Final Fix
            rigid1.set_position(a1.position)

    # Fix both colliders
    else:
        # Currently do nothing
        pass


def _resolve2d_circle_circle(a1: Collider_Circle_2D, a2: Collider_Circle_2D, rigid1: Rigidbody, rigid2: Rigidbody):
    pass

