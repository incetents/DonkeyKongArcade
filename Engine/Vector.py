
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

from __future__ import annotations
import math


class Vector2:
    # Create with 2 floats
    def __init__(self, _x: float=0, _y: float=0):
        self.x: float = _x
        self.y: float = _y

    # Convert to another Vector
    def get_vec3(self) -> Vector3:
        return Vector3(self.x, self.y, 0)

    def get_vec4(self) -> Vector4:
        return Vector4(self.x, self.y, 0, 0)

    # Magnitude / Length
    def magnitude(self) -> float:
        return math.sqrt(self.x*self.x + self.y*self.y)

    def length(self) -> float:
        return self.magnitude()

    # Normalize
    def normalize(self):
        _mag = self.magnitude()
        if _mag is 0:
            return Vector3()

        self.x /= _mag
        self.y /= _mag
        return self

    # Multiply with other vector
    def mult(self, other: Vector2) -> Vector2:
        return Vector2(self.x * other.x, self.y * other.y)

    @staticmethod
    def get_rotation(angle: float):
        return Vector2(
            math.sin(math.radians(angle)),
            math.cos(math.radians(angle))
        )

    # [str] string overload
    def __str__(self):
        return str(self.x) + ' ' + str(self.y)

    # [] overload -> get
    def __getitem__(self, index: int) -> float:
        if index is 0:
            return self.x
        else:
            return self.y

    # [] overload -> set
    def __setitem__(self, index, value):
        if index is 0:
            self.x = value
        else:
            self.y = value

    # [ + ] overload
    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)

    # [ += ] overload
    def __iadd__(self, other: Vector2) -> Vector2:
        self.x += other.x
        self.y += other.y
        return self

    # [ - ] overload
    def __sub__(self, other: Vector2) -> Vector2:
        return Vector2(self.x - other.x, self.y - other.y)

    # [ -= ] overload
    def __isub__(self, other: Vector2) -> Vector2:
        self.x -= other.x
        self.y -= other.y
        return self

    # [ -(vector) ] overload
    def __neg__(self) -> Vector2:
        self.x = -self.x
        self.y = -self.y
        return self

    # [ * float ] overload
    def __mul__(self, other: float) -> Vector2:
        return Vector2(self.x * other, self.y * other)

    # [ *= float ] overload
    def __imul__(self, other: float) -> Vector2:
        self.x *= other
        self.y *= other
        return self

    # [ / float ] overload
    def __truediv__(self, other: float):
        return Vector2(self.x / other, self.y / other)

    # [ /= float ] overload/*
    def __itruediv__(self, other: float) -> Vector2:
        self.x /= other
        self.y /= other
        return self

    # [ % ] mod overload
    def __mod__(self, other: float) -> Vector2:
        return Vector2(self.x % other, self.y % other)

    # [ %= ] mod overload
    def __imod__(self, other: float) -> Vector2:
        self.x %= other
        self.y %= other
        return self

    # [ abs() ] overload
    def __abs__(self) -> Vector2:
        self.x = abs(self.x)
        self.y = abs(self.y)
        return self

    # [ round() ] overload
    def __round__(self) -> Vector2:
        self.x = round(self.x)
        self.y = round(self.y)
        return self

    # [ floor() ] overload
    def __floor__(self) -> Vector2:
        self.x = math.floor(self.x)
        self.y = math.floor(self.y)
        return self

    # [ ceil() ] overload
    def __ceil__(self) -> Vector2:
        self.x = math.ceil(self.x)
        self.y = math.ceil(self.y)
        return self


class Vector3:
    # Create with 3 floats
    def __init__(self, _x: float=0, _y: float=0, _z: float=0):
        self.x: float = _x
        self.y: float = _y
        self.z: float = _z

    # Convert to Vectors
    def get_vec2(self) -> Vector2:
        return Vector2(self.x, self.y)

    def get_vec4(self) -> Vector4:
        return Vector4(self.x, self.y, self.z, 0)

    # Magnitude
    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def length(self) -> float:
        return self.magnitude()

    # Normalize
    def normalize(self):
        _mag = self.magnitude()
        if _mag is 0:
            return Vector3()

        self.x /= _mag
        self.y /= _mag
        self.z /= _mag
        return self

    # Multiply with other vector
    def mult(self, other: Vector3) -> Vector3:
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

    # [str] string overload
    def __str__(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.z)

    # [] overload -> get
    def __getitem__(self, index: int) -> float:
        if index is 0:
            return self.x
        elif index is 1:
            return self.y
        else:
            return self.z

    # [] overload -> set
    def __setitem__(self, index, value):
        if index is 0:
            self.x = value
        elif index is 1:
            self.y = value
        else:
            self.z = value

    # [ + ] overload
    def __add__(self, other: Vector3) -> Vector3:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    # [ += ] overload
    def __iadd__(self, other: Vector3) -> Vector3:
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    # [ - ] overload
    def __sub__(self, other: Vector3) -> Vector3:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    # [ -= ] overload
    def __isub__(self, other: Vector3) -> Vector3:
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    # [ -(vector) ] overload
    def __neg__(self) -> Vector3:
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self

    # [ * float ] overload
    def __mul__(self, other: float) -> Vector3:
        return Vector3(self.x * other, self.y * other, self.z * other)

    # [ *= float ] overload
    def __imul__(self, other: float) -> Vector3:
        self.x *= other
        self.y *= other
        self.z *= other
        return self

    # [ / float ] overload
    def __truediv__(self, other: float) -> Vector3:
        return Vector3(self.x / other, self.y / other, self.z / other)

    # [ /= float ] overload/*
    def __itruediv__(self, other: float) -> Vector3:
        self.x /= other
        self.y /= other
        self.z /= other
        return self

    # [ % ] mod overload
    def __mod__(self, other: float) -> Vector3:
        return Vector3(self.x % other, self.y % other, self.z % other)

    # [ %= ] mod overload
    def __imod__(self, other: float) -> Vector3:
        self.x %= other
        self.y %= other
        self.z %= other
        return self

    # [ abs() ] overload
    def __abs__(self) -> Vector3:
        self.x = abs(self.x)
        self.y = abs(self.y)
        self.z = abs(self.z)
        return self

    # [ round() ] overload
    def __round__(self) -> Vector3:
        self.x = round(self.x)
        self.y = round(self.y)
        self.z = round(self.z)
        return self

    # [ floor() ] overload
    def __floor__(self) -> Vector3:
        self.x = math.floor(self.x)
        self.y = math.floor(self.y)
        self.z = math.floor(self.z)
        return self

    # [ ceil() ] overload
    def __ceil__(self) -> Vector3:
        self.x = math.ceil(self.x)
        self.y = math.ceil(self.y)
        self.z = math.ceil(self.z)
        return self


class Vector4:
    # Create with 4 floats
    def __init__(self, _x: float=0, _y: float=0, _z: float=0, _w: float= 0):
        self.x: float = _x
        self.y: float = _y
        self.z: float = _z
        self.w: float = _w

    # Convert to another Vector
    def get_vec2(self) -> Vector2:
        return Vector2(self.x, self.y)

    def get_vec3(self) -> Vector3:
        return Vector3(self.x, self.y, self.z)



