
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Render multiple sprites at once

from Engine.Texture import *
from Engine.Entity import *
from Engine.Vector import *
from typing import *


class SpriteBatch:
    def __init__(self, batch_name: str, sprite_ref: str):
        self.name: str = batch_name
        self._sprite_ref: Sprite = Engine.Storage.get(Engine.Storage.Type.SPRITE, sprite_ref)
        self._entities: List[Entity] = []
        self._vertices: List[Tuple[Vector2, Vector2, Vector2, Vector2]] =\
            [Tuple[Vector2, Vector2, Vector2, Vector2]]
        self._dirty = True

        self._temp_flip: Vector2 = None
        self._temp_half_size: Vector2 = None
        self._temp_offset: Vector2 = None
        self._update_temp()

    def get_size(self) -> int:
        return len(self._entities)

    def get_sprite(self) -> Sprite:
        return self._sprite_ref

    def get_entities(self) -> List[Entity]:
        return self._entities

    def set_sprite(self, sprite_ref: str):
        self._sprite_ref: Sprite = Engine.Storage.get(Engine.Storage.Type.SPRITE, sprite_ref)
        self._update_temp()
        return self

    def add_entity(self, entity: Entity):
        self._entities.append(entity)
        self._dirty = True
        return self

    def clear(self):
        self._entities.clear()
        return self

    def _update_temp(self):
        self._temp_flip = Vector2(
            -1.0 if self._sprite_ref._flip[0] is True else 1.0,
            -1.0 if self._sprite_ref._flip[0] is True else 1.0
        )
        self._temp_half_size = self._sprite_ref.get_scale_half()
        self._temp_offset = self._sprite_ref.get_offset()

    def _recalculate(self, _index: int):
        # Model Scale
        model: Transform = self._entities[_index].transform

        _pos = model.get_position().get_vec2()
        _scale = model.get_scale_fixed().get_vec2()

        _verts: List[Vector2] = self._sprite_ref.get_local_vertices()

        _p1 = _verts[0].mult(_scale) + _pos
        _p2 = _verts[1].mult(_scale) + _pos
        _p3 = _verts[2].mult(_scale) + _pos
        _p4 = _verts[3].mult(_scale) + _pos

        self._vertices[_index] = _p1, _p2, _p3, _p4

    def _recalculate_all(self):
        if self._dirty is False:
            return
#
        self._vertices.clear()
        self._dirty = False

        # Padd with empty values
        for i in self._entities:
            self._vertices.append([Vector2(), Vector2(), Vector2(), Vector2()])

        # Fix values at correct locations
        for i in range(len(self._entities)):
            self._recalculate(i)

    def draw(self):
        # Recalculate Positions if changed
        if self._dirty is True:
            self._recalculate_all()

        # Texture
        if self._sprite_ref is None:
            print("Missing Group Texture")
            return

        self._sprite_ref.get_texture().bind()

        # Uvs
        _uvs: Vector4 = self._sprite_ref.get_uvs()

        # Quad
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBegin(GL_QUADS)
        glColor(1, 1, 1, 1)

        for i in range(len(self._vertices)):

            # Check if value has changed and fix it
            if self._entities[i].transform.dirty:
                self._recalculate(i)
                self._entities[i].transform.dirty = False

            _values: Tuple[Vector2, Vector2, Vector2, Vector2] = self._vertices[i]

            glTexCoord2f(_uvs.x, _uvs.z)
            glVertex2f(_values[0].x, _values[0].y)

            glTexCoord2f(_uvs.y, _uvs.z)
            glVertex2f(_values[1].x, _values[1].y)

            glTexCoord2f(_uvs.y, _uvs.w)
            glVertex2f(_values[2].x, _values[2].y)

            glTexCoord2f(_uvs.x, _uvs.w)
            glVertex2f(_values[3].x, _values[3].y)

        glEnd()

    def __len__(self) -> int:
        return len(self._entities)
