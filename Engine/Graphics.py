
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Drawing Shapes]

from enum import Enum

from Engine.Vector import *
from Engine.Transform import *
import Engine.Storage

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import Engine.Config


def set_clear_color(color: Vector4):
    Engine.Config.CLEAR_COLOR = color

def clear_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(
        Engine.Config.CLEAR_COLOR.x,
        Engine.Config.CLEAR_COLOR.y,
        Engine.Config.CLEAR_COLOR.z,
        Engine.Config.CLEAR_COLOR.w
    )


class Debug:
    def __init__(self):
        pass

    @staticmethod
    def draw_line_2d(_pos1: Vector2, _pos2: Vector2, _color: Vector3, _depth: float=0):
        glDisable(GL_BLEND)
        glBegin(GL_LINES)
        glColor(_color.x, _color.y, _color.z, 1)
        glVertex3f(_pos1.x, _pos1.y, _depth)
        glVertex3f(_pos2.x, _pos2.y, _depth)
        glEnd()

    @staticmethod
    def draw_line_3d(_pos1: Vector3, _pos2: Vector3, _color: Vector3):
        glDisable(GL_BLEND)
        glBegin(GL_LINES)
        glColor(_color.x, _color.y, _color.z, 1)
        glVertex3f(_pos1.x, _pos1.y, _pos1.z)
        glVertex3f(_pos2.x, _pos2.y, _pos2.z)
        glEnd()

    @staticmethod
    def draw_circle_2d(_pos, _radius: float, _color: Vector3, _vertices: int = 40):
        glDisable(GL_BLEND)
        glBegin(GL_LINE_LOOP)
        glColor(_color.x, _color.y, _color.z, 1)
        for i in range(_vertices):
            _vec = Vector2.get_rotation(360 * (i / _vertices))
            glVertex2f(_pos.x + _vec.x * _radius, _pos.y + _vec.y * _radius)

        glEnd()

    @staticmethod
    def draw_square_2d(_pos, _size, _color: Vector3):
        _left_x = _pos.x - _size.x * 0.5
        _right_x = _pos.x + _size.x * 0.5
        _down_y = _pos.y - _size.y * 0.5
        _up_y = _pos.y + _size.y * 0.5

        glDisable(GL_BLEND)
        glBegin(GL_LINE_LOOP)
        glColor(_color.x, _color.y, _color.z, 1)
        glVertex2f(_left_x, _down_y)
        glVertex2f(_right_x, _down_y)
        glVertex2f(_right_x, _up_y)
        glVertex2f(_left_x, _up_y)
        glEnd()


class MeshMode(Enum):
    NONE = 0,
    TEXTURED = 1,
    COLORED = 2


class Mesh:
    def __init__(self, mesh_name: str):
        # self._position: Vector3 = Vector3()
        # self._rotationVector: Vector3 = Vector3(0, 0, 1)
        # self._rotationAmount: float = 0
        # self._scale: Vector3 = Vector3(50, 50, 50)
        # Data Buffers
        self._mode: MeshMode = MeshMode.NONE
        self._drawCount: int = 0
        self._vertices: Vector3 = []
        self._uvs: Vector2 = []
        self._colors: Vector3 = []
        # Add to Storage
        Engine.Storage.add(Engine.Storage.Type.MESH, mesh_name, self)

    # Setters
    def set_vertices(self, vertices: Vector3 = List[Vector3]):
        self._vertices = vertices
        self._drawCount = len(vertices)

    def set_uvs(self, uvs: Vector2 = List[Vector2]):
        if len(uvs) is self._drawCount:
            self._uvs = uvs
            self._mode = MeshMode.TEXTURED
        else:
            print('Cannot assign uvs without matching amount of vertices')

    def set_colors(self, colors: Vector3 = List[Vector3]):
        if len(colors) is self._drawCount:
            self._colors = colors
            self._mode = MeshMode.COLORED
        else:
            print('Cannot assign colors without matching amount of vertices')

    def draw(self, _model: Transform):
         # Set Blend Mode
         if self._mode is MeshMode.TEXTURED:
             glEnable(GL_BLEND)
         else:
             glDisable(GL_BLEND)

         # Draw Mesh
         glPushMatrix()

         # Apply Transformation
         _model.apply()

         glBegin(GL_QUADS)

         if self._mode is MeshMode.NONE:
            glColor3f(0, 0, 0)
            for i in range(self._drawCount):
                glVertex3f(self._vertices[i].x, self._vertices[i].y, self._vertices[i].z)

         elif self._mode is MeshMode.COLORED:
            for i in range(self._drawCount):
                glColor(self._colors[i].x, self._colors[i].y, self._colors[i].z, 1.0)
                glVertex3f(self._vertices[i].x, self._vertices[i].y, self._vertices[i].z)

         elif self._mode is MeshMode.TEXTURED:
            glColor(1, 1, 1, 1)
            for i in range(self._drawCount):
                glTexCoord2f(self._uvs[i].x, self._uvs[i].y)
                glVertex3f(self._vertices[i].x, self._vertices[i].y, self._vertices[i].z)

         glEnd()
         glPopMatrix()
