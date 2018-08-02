
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Render multiple sprites at once

from Engine.Texture import *
from Engine.Entity import *
from typing import *


class SpriteBatch:
    def __init__(self, sprite_ref: str):
        self._sprite_ref: Sprite = Engine.Storage.get(Engine.Storage.Type.SPRITE, sprite_ref)
        self._models: List[Transform] = []

    def set_sprite(self, sprite_ref: str):
        self._sprite_ref: Sprite = Engine.Storage.get(Engine.Storage.Type.SPRITE, sprite_ref)

    def add_model(self, model: Transform):
        self._models.append(model)

    def clear(self):
        self._models.clear()

    def draw(self):
        # Texture
        if self._sprite_ref is None:
            print("Missing Group Texture")
            return

        self._sprite_ref.get_texture().bind()

        _offset = self._sprite_ref.get_offset()
        _spr_size_half = Vector2(self._sprite_ref.get_width_half(), self._sprite_ref.get_height_half())

        # Quad
        glEnable(GL_BLEND)
        glBegin(GL_QUADS)
        glColor(1, 1, 1, 1)

        for i in self._models:

            # Model Scale
            _xscale = i._scale.x * i.get_flip_x()
            _yscale = i._scale.y * i.get_flip_y()

            glTexCoord2f(0, 0)
            glVertex2f(
                (_spr_size_half.x * (_offset.x - _xscale)) + i.get_position().x,
                (_spr_size_half.y * (_offset.y - _yscale)) + i.get_position().y
            )

            glTexCoord2f(1, 0)
            glVertex2f(
                (_spr_size_half.x * (_offset.x + _xscale)) + i.get_position().x,
                (_spr_size_half.y * (_offset.y - _yscale)) + i.get_position().y
            )

            glTexCoord2f(1, 1)
            glVertex2f(
                (_spr_size_half.x * (_offset.x + _xscale)) + i.get_position().x,
                (_spr_size_half.y * (_offset.y + _yscale)) + i.get_position().y
            )

            glTexCoord2f(0, 1)
            glVertex2f(
                (_spr_size_half.x * (_offset.x - _xscale)) + i.get_position().x,
                (_spr_size_half.y * (_offset.y + _yscale)) + i.get_position().y
            )

        glEnd()