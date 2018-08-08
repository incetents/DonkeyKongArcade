
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
TRIGGER_ID_FIRE_BARREL = 4
TRIGGER_ID_WIN = 8
TRIGGER_ID_WALL = 16
TRIGGER_ID_MARIO = 32
TRIGGER_ID_BARREL = 64
