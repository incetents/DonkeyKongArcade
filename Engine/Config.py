
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Window Data to display game

from Engine.Vector import *

# Original Game (224/256) Scaled x3 = (672/768)
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

CLEAR_COLOR = Vector4(0, 0, 0, 1)

TILE_SIZE = 8

GRAV = 100

# Different types of ids for collisions
TRIGGER_ID_NONE = 0
TRIGGER_ID_LADDER = 1
TRIGGER_ID_DEATH = 2
TRIGGER_ID_OIL_BARREL = 4
TRIGGER_ID_BARREL_DESTROY = 8
TRIGGER_ID_WIN = 16
TRIGGER_ID_WALL = 32
TRIGGER_ID_BARREL = 64
TRIGGER_ID_MARIO = 128
TRIGGER_ID_FLOOR = 256
TRIGGER_ID_FLAME = 512
