
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Static Dictionaries of different data]

from enum import Enum
from Engine.Texture import Texture


class Type(Enum):
    TEXTURE = 1,
    MESH = 2,
    SPRITE = 3
    SPRITE_SEQUENCE = 4
    Entity = 5,
    SONG = 6,
    SFX = 7


# Main Storage
Storage = {
    Type.TEXTURE: {},
    Type.MESH: {},
    Type.SPRITE: {},
    Type.SPRITE_SEQUENCE: {},
    Type.Entity: {},
    Type.SONG: {},
    Type.SFX: {}
}


# !!! Add also overrides if names are duplicates
def add(_type: Type, _name: str, _data):
    global Storage
    Storage[_type][_name] = _data


def get(_type: Type, _name: str):
    # Exception
    if _name is '':
        return None

    # Grab Data
    global Storage
    if _name in Storage[_type]:
        _data = Storage[_type][_name]
        return _data
    # Data not found
    else:
        print('Storage Get Error, type:', _type, ',name:', _name)
        return None
