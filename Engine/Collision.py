

# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Colliders]

from __future__ import annotations
import math
from functools import singledispatch
from typing import *
from enum import Enum
from Engine.Vector import Vector2, Vector3
from Engine.Graphics import Debug
from Engine.Rigidbody import Rigidbody
from Engine.Transform import *
from Engine.Sprite import *
from Engine.Config import *

# Collision Checking Classes
#
class Collision_Type(Enum):
    SOLID = 1,
    TRIGGER = 2,
    PLATFORM = 3,

# 1D Collision General Use
#

# Assumes p1 is smaller than p2 for both lines
def collision_1D_unsafe(line1_p1: float, line1_p2: float, line2_p1: float, line2_p2: float) -> bool:
    # Check intersection
    return line1_p2 >= line2_p1 and line2_p2 >= line1_p1

# Assumes that lines could be backwards
def collision_1D_safe(line1_p1: float, line1_p2: float, line2_p1: float, line2_p2: float) -> bool:
    # Check End points of lines
    _min_line1 = min(line1_p1, line1_p2)
    _max_line1 = max(line1_p1, line1_p2)
    _min_line2 = min(line2_p1, line2_p2)
    _max_line2 = max(line2_p1, line2_p2)
    # Check intersection
    return collision_1D_unsafe(_min_line1, _max_line1, _min_line2, _max_line2)

# Checks if two lines intersect and return the resulting point if they do
def line_to_line_collision(a1: Vector2, a2: Vector2, b1: Vector2, b2: Vector2) -> Tuple[Vector2, bool]:
    b: Vector2 = a2 - a1
    d: Vector2 = b2 - b1
    bDotDPerp = b.x * d.y - b.y * d.x
    if bDotDPerp == 0:
        return Vector2(), False

    c = b1 - a1

    t: float = (c.x * d.y - c.y * d.x) / bDotDPerp
    if t < 0 or t > 1:
        return Vector2(), False

    u: float = (c.x * b.y - c.y * b.x) / bDotDPerp
    if u < 0 or u > 1:
        return Vector2(), False

    out_result = a1 + b * t
    return out_result, True


class Collider(Component):
    def __init__(self, position: Vector3):
        super().__init__()
        self._position: Vector3 = position
        self.offset: Vector2 = Vector2()
        self.enabled: bool = True
        self.id: int = Engine.Config.TRIGGER_ID_NONE
        self.type: Collision_Type = Collision_Type.SOLID
        self.contact_list_prev: Set[Collider] = set()
        self.contact_list: Set[Collider] = set()
        pass

    def get_position(self) -> Vector3:
        return self._position + self.offset.get_vec3()

    def get_hit_point(self, point: Vector2, direction: Vector2, distance: float):
        print("""Err, get_hit_point doesn't work on simple collider""")

    def check_if_point_inside(self, point: Vector2):
        print("""Err, check_if_point_inside doesn't work on simple collider""")

    def check_if_line_inside(self, p1: Vector2, p2: Vector2):
        print("""Err, check_if_line_inside doesn't work on simple collider""")

    # Virtual
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

    def get_hit_point(self, point: Vector2, direction: Vector2, distance: float):
        print('not implemented')
        pass

    def check_if_point_inside(self, point: Vector2):
        _pos = self.get_position().get_vec2()
        return (_pos - point).magnitude() <= self.radius

    def check_if_line_inside(self, p1: Vector2, p2: Vector2):
        print('not implemented')
        pass

    def draw(self, _color: Vector3 = Vector3(0, 1, 0), _vertices:int = 40):
        Debug.draw_circle_2d(self.get_position(), self.radius, _color, _vertices)


class Collider_AABB_2D(Collider):
    def __init__(self, pos: Vector3, size: Vector3=Vector3()):
        Collider.__init__(self, pos)
        self.size: Vector2 = size

    def set_size_from_sprite(self, model: Transform, spr: Sprite):
        self.size = model.get_scale().get_vec2().mult(spr.get_scale())

    def get_hit_point(self, point: Vector2, direction: Vector2, distance: float) -> Tuple[Vector2, bool]:
        # Make sure point is outside box
        if self.check_if_point_inside(point):
            return Vector2(), False

        # Intersection
        # Line to line with all 4 sides#
        _topleft = Vector2(self.get_left(), self.get_up())
        _topright = Vector2(self.get_right(), self.get_up())
        _botleft = Vector2(self.get_left(), self.get_down())
        _botright = Vector2(self.get_right(), self.get_down())

        _p2 = point + direction * distance

        _mem: Tuple[Vector2, bool] = line_to_line_collision(point, _p2, _topleft, _topright)
        if _mem[1]:
            return _mem[0], True

        _mem: Tuple[Vector2, bool] = line_to_line_collision(point, _p2, _topleft, _botleft)
        if _mem[1]:
            return _mem[0], True

        _mem: Tuple[Vector2, bool] = line_to_line_collision(point, _p2, _botright, _topright)
        if _mem[1]:
            return _mem[0], True

        _mem: Tuple[Vector2, bool] = line_to_line_collision(point, _p2, _botright, _botleft)
        if _mem[1]:
            return _mem[0], True

        return Vector2(), False

    def check_if_point_inside(self, point: Vector2):
        # Check if point is inside the aabb collider
        return self.get_left() < point.x < self.get_right() and self.get_down() < point.y < self.get_up()

    def check_if_line_inside(self, p1: Vector2, p2: Vector2):
        # Check if either end points are located inside
        if self.check_if_point_inside(p1) or self.check_if_point_inside(p2):
            # print('inside box, simple collision')
            return True

        # Solve y = mx + b  for straight line (m = slope, b = vertical offset)
        _direction = p2 - p1
        _m = 0.0
        if _direction.x != 0:
            _m = _direction.y / _direction.x

        # Vertical Slope possibility
        else:
            return collision_1D_unsafe(
                self.get_down(), self.get_up(),
                min(p1.y, p2.y), max(p1.y, p2.y))


        _b = p1.y - _m * p1.x # (y - mx = b)
        # Check for y values when x is at left or right of square
        _y1 = _m * self.get_left() + _b
        _y2 = _m * self.get_right() + _b
        # Check for x values when y is top or down (x = (y-b)/m)
        _x1 = (self.get_up() - _b) / _m
        _x2 = (self.get_down() - _b) / _m

        # Check if y values are between y values
        if self.get_down() < _y1 < self.get_up() or self.get_down() < _y2 < self.get_up():
            return True

        if self.get_left() < _x1 < self.get_right() or self.get_left() < _x2 < self.get_right():
            return True

        return False

    def get_left(self) -> float:
        return self._position.x - (self.size.x * 0.5) + self.offset.x

    def get_right(self) -> float:
        return self._position.x + (self.size.x * 0.5) + self.offset.x

    def get_up(self) -> float:
        return self._position.y + (self.size.y * 0.5) + self.offset.y

    def get_down(self) -> float:
        return self._position.y - (self.size.y * 0.5) + self.offset.y

    def draw(self, _color: Vector3 = Vector3(0, 1, 0)):
        Debug.draw_square_2d(self.get_position(), self.size, _color)


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
    _x_intersection = collision_1D_unsafe(a1.get_left(), a1.get_right(), a2.get_left(), a2.get_right())
    if _x_intersection is False:
        return False
    _y_intersection = collision_1D_unsafe(a1.get_down(), a1.get_up(), a2.get_down(), a2.get_up())
    return _y_intersection


def _check2d_circle_circle(c1: Collider_Circle_2D, c2: Collider_Circle_2D) -> bool:
    _radius_total = c1.radius + c2.radius
    _distance = (c1.get_position() - c2.get_position()).magnitude()
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


def _resolve2d_aabb_aabb(collider1: Collider_AABB_2D, collider2: Collider_AABB_2D, rigid1: Rigidbody, rigid2: Rigidbody):
    # Error
    if rigid1 is None:
        return

    # Fix only first collider
    if rigid2 is None:

        # Initial Position Fix
        collider1.position = rigid1.get_position()

        # Correct Positions (due to collider class having offsets internally)
        _a = collider1.get_position().get_vec2()
        _b = collider2.get_position().get_vec2()

        # Platform Collision
        if collider2.type is Collision_Type.PLATFORM:
            if collider1.get_down() >= _b.y and rigid1.get_velocity().y <= 0:
                collider1.position.y += collider2.get_up() - collider1.get_down()
                # Vel can only go up
                rigid1.set_vel_y(max(0, rigid1.get_velocity().y))
            pass

        # Normal Collision
        elif collider2.type is Collision_Type.SOLID:
            # Check depth of X and Y intersection
            _xdepth: int = 0
            _ydepth: int = 0
            _left: bool
            _up: bool

            # Check X position
            if _a.x < _b.x:
                # Depth
                _left = True
                _xdepth = collider1.get_right() - collider2.get_left()
            else:
                # Depth
                _left = False
                _xdepth = collider2.get_right() - collider1.get_left()

            # Check Y position
            if _a.y < _b.y:
                # Depth
                _up = False
                _ydepth = collider1.get_up() - collider2.get_down()
            else:
                # Depth
                _up = True
                _ydepth = collider2.get_up() - collider1.get_down()

            # Fix X-axis
            if _xdepth < _ydepth:
                if _left and rigid1.get_velocity().x > 0:
                    collider1.position.x -= _xdepth
                    # Vel can only go left
                    rigid1.set_vel_x(min(0, rigid1.get_velocity().x))
                elif not _left and rigid1.get_velocity().x < 0:
                    collider1.position.x += _xdepth
                    # Vel can only go right
                    rigid1.set_vel_x(max(0, rigid1.get_velocity().x))
            # Fix Y-axis
            else:
                if _up and rigid1.get_velocity().y < 0:
                    collider1.position.y += _ydepth
                    # Vel can only go up
                    rigid1.set_vel_y(max(0, rigid1.get_velocity().y))
                elif not _up and rigid1.get_velocity().y > 0:
                    collider1.position.y -= _ydepth
                    # Vel can only go down
                    rigid1.set_vel_y(min(0, rigid1.get_velocity().y))

        # Final Fix
        rigid1.set_position(collider1.position)

    # Fix both colliders
    else:
        # Currently do nothing
        pass




def _resolve2d_circle_circle(a1: Collider_Circle_2D, a2: Collider_Circle_2D, rigid1: Rigidbody, rigid2: Rigidbody):
    pass

