
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [loading and binding textures]

# Imports
import Engine.Storage
from enum import Enum
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


class FilterMode(Enum):
    POINT = 1,
    LINEAR = 2


FilterLookup = {
    FilterMode.POINT: GL_NEAREST,
    FilterMode.LINEAR: GL_LINEAR
}


class WrapMode(Enum):
    CLAMP = 1,
    REPEAT = 2


WrapLookup = {
    WrapMode.CLAMP: GL_CLAMP,
    WrapMode.REPEAT: GL_REPEAT
}

# Static Lookup Table of Textures
# Lookup = {}


class Texture:
    def __init__(self, tex_name: str, file_path: str,filter_mode: FilterMode=FilterMode.LINEAR,
                 wrap_mode: WrapMode=WrapMode.REPEAT):
        # Data
        self._id = glGenTextures(1)
        self._name: str = tex_name
        self._width: int = 0
        self._height: int = 0
        self._img_load: pygame.Surface = None
        self._img_raw: str = None
        # Load Image Section
        self.load(tex_name, file_path, filter_mode, wrap_mode)

    def load(self, tex_name: str, file_path: str, filter_mode: FilterMode, wrap_mode: WrapMode):
        # Load And Store Data
        self._img_load: pygame.Surface = None
        try:
            self._img_load = pygame.image.load(file_path)
        except:
            print('unable to load filepath: ', file_path)
            return

        self._img_raw = pygame.image.tostring(self._img_load, "RGBA", 1)
        self._width = self._img_load.get_width()
        self._height = self._img_load.get_height()
        # Load Texture in GPU
        glBindTexture(GL_TEXTURE_2D, self._id)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, FilterLookup[filter_mode])
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, FilterLookup[filter_mode])
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, WrapLookup[wrap_mode])
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, WrapLookup[wrap_mode])
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self._width, self._height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self._img_raw)
        # Add to List of all textures
        # global Lookup
        # Lookup[tex_name] = self
        # Storage.add_texture(tex_name, self)
        Engine.Storage.add(Engine.Storage.Type.TEXTURE, tex_name, self)

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self._id)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height






