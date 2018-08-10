
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Render multiple sprites at once

from Engine.Texture import *
from Engine.Entity import *
from Engine.Vector import *
from typing import *


class SpriteBatch:
    def __init__(self, batch_name: str, texture_name: str):
        self.name: str = batch_name
        self._texture: Texture = Engine.Storage.get(Engine.Storage.Type.TEXTURE, texture_name)
        self._entities: List[Entity] = []
        self._sprites_ref: List[Sprite] = []

    def get_texture(self):
        return self._texture

    def get_size(self) -> int:
        return len(self._entities)

    def get_entities(self) -> List[Entity]:
        return self._entities

    def set_texture(self, texture: Texture):
        self._texture = texture

    def add_entities(self, entities: List[Entity]):
        e: Entity
        for e in entities:
            self.add_entity(e)

    def add_entity(self, entity: Entity):
        # Make sure it has a sprite
        _spr = entity.get_component(Sprite)
        if _spr is not None:
            self._entities.append(entity)
            self._sprites_ref.append(_spr)
        else:
            print('cannot add entity to sprite batch because its missing a sprite', entity)
        return self

    def clear(self):
        self._entities.clear()
        self._sprites_ref.clear()
        return self

    def draw(self):
        # Check Texture
        if self._texture is None:
            print("Missing Group Texture")
            return
        # Place Texture on all items
        self._texture.bind()

        # Quad
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBegin(GL_QUADS)
        glColor(1.0, 1.0, 1.0, 1.0)

        for i in range(len(self._sprites_ref)):
            # Get Model
            _model: Transform = self._entities[i].transform
            # Draw Sprite
            self._sprites_ref[i]._calculate_local_vertices()
            self._sprites_ref[i]._draw_legacy(_model)

        glEnd()

    def __len__(self) -> int:
        return len(self._entities)
