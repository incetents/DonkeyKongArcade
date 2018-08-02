
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# 2D Sprites

from Engine.Texture import Texture
from Engine.Graphics import Mesh
from Engine.Vector import *
from Engine.Transform import *
from Engine.Graphics import *
from Engine.Anchor import *
import Engine.Anchor
import Engine.Storage
from OpenGL.GL import *
from typing import List, Dict
import math


class Sprite:
    def __init__(self, sprite_name: str, texture_name: str, _anchor: Anchor=Anchor.MID):
        self._texture: Texture = Engine.Storage.get(Engine.Storage.Type.TEXTURE, texture_name)
        if self._texture is None:
            print('ERR CANNOT FIND TEX: ', texture_name, ' for Sprite')
            exit(0)
        self._tex_width: int = self._texture.get_width()
        self._tex_height: int = self._texture.get_height()
        self._tex_w_half: float = self._tex_width * 0.5
        self._tex_h_half: float = self._tex_height * 0.5
        self._flip: List[bool] = [False, False]
        self._offset: Vector2 = Vector2()
        self.set_anchor(_anchor)
        # Add Sprite to Storage
        Engine.Storage.add(Engine.Storage.Type.SPRITE, sprite_name, self)

    def set_anchor(self, _anchor: Anchor):
        self._offset = Vector2(-Engine.Anchor._AnchorValues[_anchor][0], -Engine.Anchor._AnchorValues[_anchor][1])
        return self

    def set_flip_x(self, state: bool):
        self._flip[0] = state
        return self

    def set_flip_y(self, state: bool):
        self._flip[1] = state
        return self

    def get_offset(self) -> Vector2:
        return self._offset

    def get_texture(self) -> Texture:
        return self._texture

    def get_width(self) -> float:
        return self._tex_width

    def get_width_half(self) -> float:
        return self._tex_w_half

    def get_height(self) -> float:
        return self._tex_height

    def get_height_half(self) -> float:
        return self._tex_h_half

    def get_anchor(self, _anchor: Anchor, _model: Transform) -> Vector2:
        return _model.get_position().get_vec2() + \
               Vector2(
                   _model.get_scale().y * self._tex_w_half * (self._offset.x + Engine.Anchor._AnchorValues[_anchor][0]),
                   _model.get_scale().x * self._tex_h_half * (self._offset.y + Engine.Anchor._AnchorValues[_anchor][1])
               )

    def draw(self, _model: Transform):
        # Texture
        self._texture.bind()

        # Quad
        glEnable(GL_BLEND)
        glBegin(GL_QUADS)
        glColor4f(1,1,1,1)

        _xscale = _model._scale.x * _model.get_flip_x() * (-1.0 if self._flip[0] is True else 1.0)
        _yscale = _model._scale.y * _model.get_flip_y() * (-1.0 if self._flip[1] is True else 1.0)

        # Bottom Left
        glTexCoord2f(0, 0)
        glVertex2f(
            (self._tex_w_half * (self._offset.x -_xscale)) + _model._position.x,
            (self._tex_h_half * (self._offset.y -_yscale)) + _model._position.y
        )

        # Bottom Right
        glTexCoord2f(1, 0)
        glVertex2f(
            (self._tex_w_half * (self._offset.x +_xscale)) + _model._position.x,
            (self._tex_h_half * (self._offset.y -_yscale)) + _model._position.y
        )

        # Top Right
        glTexCoord2f(1, 1)
        glVertex2f(
            (self._tex_w_half * (self._offset.x +_xscale)) + _model._position.x,
            (self._tex_h_half * (self._offset.y +_yscale)) + _model._position.y
        )

        # Top Left
        glTexCoord2f(0, 1)
        glVertex2f(
            (self._tex_w_half * (self._offset.x -_xscale)) + _model._position.x,
            (self._tex_h_half * (self._offset.y +_yscale)) + _model._position.y
        )

        glEnd()


class SpriteSequence:
    def __init__(self, animation_name: str, *sprite_names: str):
        self._sprites: List[Sprite] = []
        self.speed = 1.0
        for i in sprite_names:
            self.add_sprite(i)
        # Add to Storage
        Engine.Storage.add(Engine.Storage.Type.SPRITE_SEQUENCE, animation_name, self)

    def add_sprite(self, sprite_name):
        _spr: Sprite = Engine.Storage.get(Engine.Storage.Type.SPRITE, sprite_name)
        if _spr is not None and _spr not in self._sprites:
            self._sprites.append(_spr)

    def __len__(self):
        return len(self._sprites)

    def __getitem__(self, index):
        return self._sprites[index]


class SpriteAnimation:
    def __init__(self, *sequence_names: str):
        self._sequences: Dict[str, SpriteSequence] = {}
        self._current_sequence: SpriteSequence = None
        self._current_sprite: Sprite = None
        self._speed: float = 1.0
        self._time_index: float = 0.0
        self._flips: List[bool] = [False, False]
        for i in sequence_names:
            self.add_sprite_sequence(i)
        if len(self._sequences) is 0:
            print("Sprite Animation Has No Sprite Sequences")
        else:
            self._current_sequence = next(iter(self._sequences.values()))
            self._current_sprite = self._current_sequence[0]

    def add_sprite_sequence(self, sequence_name: str):
        _spr: Sprite = Engine.Storage.get(Engine.Storage.Type.SPRITE_SEQUENCE, sequence_name)
        if _spr is not None and _spr not in self._sequences:
            # print('added sequence:', sequence_name)
            self._sequences[sequence_name] = _spr
        else:
            print('could not find sequence:', sequence_name)

    def set_sprite_sequence(self, sequence_name: str):
        # If sequence missing, add it
        if sequence_name not in self._sequences:
            self.add_sprite_sequence(sequence_name)
        # Set Sequence
        self._current_sequence = self._sequences[sequence_name]
        # Reset index/time
        self._time_index = 0.0

    def set_speed(self, _speed: float):
        self._speed = _speed

    def set_flip_x(self, state: bool):
        self._flips[0] = state

    def set_flip_y(self, state: bool):
        self._flips[1] = state

    def get_current_frame(self) -> Sprite:
        return self._current_sprite

    def update(self, delta_time):
        # Increment Time
        self._time_index = (self._time_index + delta_time * self._speed * self._current_sequence.speed) % len(self._current_sequence)
        # Fix Negative
        if self._time_index < 0:
            self._time_index += len(self._current_sequence)

        _index = math.floor(self._time_index)
        # Set Current Sprite
        self._current_sprite = self._current_sequence[_index]
        pass

    def draw(self, model: Transform):
        if self._current_sprite is not None:
            self._current_sprite.draw(model)



