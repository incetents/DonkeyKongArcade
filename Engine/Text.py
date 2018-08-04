
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Text to display on screen - custom drawing

from Engine.Vector import Vector2, Vector3, Vector4
import Engine.Storage
from typing import List, Dict
from OpenGL.GL import *
from enum import Enum
import math


class TextAlignment(Enum):
    LEFT = 1,
    MIDDLE = 2,
    RIGHT = 3


class TextCharacter:
    def __init__(self, uvs: Vector4):
        self._uvs: Vector4 = uvs

    def draw(self, position: Vector2):
        # Bottom Left
        glTexCoord2f(self._uvs.x, self._uvs.z)
        glVertex2f(+0.00 + position.x, +0.00 + position.y)
        # Bottom Right
        glTexCoord2f(self._uvs.y, self._uvs.z)
        glVertex2f(+0.43 + position.x, +0.00 + position.y)
        # Top Right
        glTexCoord2f(self._uvs.y, self._uvs.w)
        glVertex2f(+0.43 + position.x, +0.60 + position.y)
        # Top Left
        glTexCoord2f(self._uvs.x, self._uvs.w)
        glVertex2f(+0.00 + position.x, +0.60 + position.y)


font_char_list = """abcdefghijklmnopqrstuvwxyzàâéîô&1234567890($£.,!?)-:'[]*/"""
font_char_width = 10.0
font_char_height = 6.0
font_chars: Dict[str, TextCharacter] = {}
_temp: float = 0
for i in font_char_list:
    font_chars[i] = TextCharacter(Vector4(
        (((_temp % font_char_width) + 0.0) / font_char_width),
        (((_temp % font_char_width) + 1.0) / font_char_width),
        (math.floor(_temp / font_char_width) + 0.0) / font_char_height,
        (math.floor(_temp / font_char_width) + 1.0) / font_char_height
    ))
    _temp += 1.0


class Text:
    def __init__(self,
                 text: str,
                 position: Vector2,
                 size: float,
                 color: Vector4=Vector4(1,1,1,1),
                 alignment: TextAlignment = TextAlignment.LEFT,
                 line_length: int = 12,
                 vertical_space: float = 1.0
                 ):
        self._text: str = text.lower()
        self._text_positions: List[Vector2] = []
        self._position: Vector2 = position
        self._size: float = size
        self._color: Vector4 = color
        self._line_length: int = line_length
        self._vertical_space: float = vertical_space
        self._alignment: TextAlignment = alignment
        self._smallest_line_length: int = 0
        self._update()
        # Encrypt text

    def _update(self):
        # Update Line Length
        self._smallest_line_length = min(len(self._text), self._line_length)
        if self._line_length <= 0:
            self._smallest_line_length = len(self._text)
        # Update Text positions
        self._text_positions.clear()

        _letter_counter: int = 0
        _space_length: float = 0.43
        _xoffset: int = 0
        _xpos: int = 0
        _ypos: int = 0

        # Alignment changes
        if self._alignment is TextAlignment.MIDDLE:
            _xoffset = -self._smallest_line_length * _space_length * 0.5
        elif self._alignment is TextAlignment.RIGHT:
            _xoffset = -self._smallest_line_length * _space_length

        # Update letters
        for i in self._text:
            # Space Fix
            if i is ' ':
                _xpos += _space_length
                continue
            # Newline Fix
            elif i is '\n':
                _xpos = 0
                _ypos -= self._vertical_space
                _letter_counter = 0
                continue

            elif i not in font_chars:
                print('err font text,', i)
                continue

            # Update X Position
            _xchange = _xpos + _xoffset

            # Add X position
            self._text_positions.append(Vector2(_xchange, _ypos))

            # Add room for next letter
            _xpos += _space_length

            # New Line possibility
            if self._line_length > 0:
                _letter_counter += 1

                if _letter_counter >= self._smallest_line_length:
                    _letter_counter = 0
                    _xpos = 0
                    _ypos -= self._vertical_space

    def set_text(self, text: str):
        self._text: str = text
        self._update()

    def set_position(self, position: Vector2):
        self._position = position

    def set_size(self, size: float):
        self._size = size

    def set_color(self, color: Vector4):
        self._color = color

    def set_alpha(self, alpha: float):
        self._color.w = alpha

    def set_alignment(self, align: TextAlignment):
        self._alignment = align
        self._update()

    def set_vertical_space(self, space: float):
        self._vertical_space = space
        self._update()

    def draw(self):
        global font_uvs
        Engine.Storage.get(Engine.Storage.Type.TEXTURE, 'font').bind()

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glPushMatrix()

        glTranslatef(self._position.x, self._position.y, 0)
        glScalef(self._size, self._size, 1)

        glBegin(GL_QUADS)

        glColor(self._color.x, self._color.y, self._color.z, self._color.w)

        # Draw Each letter in local space with correct offsets
        pos_iter = iter(self._text_positions)

        for i in range(len(self._text)):
            _letter = self._text.__getitem__(i)
            # space exception
            if _letter is not ' ' and _letter is not '\n':
                _position = next(pos_iter)
                font_chars[_letter].draw(_position)

        glEnd()
        glPopMatrix()
        glFlush()