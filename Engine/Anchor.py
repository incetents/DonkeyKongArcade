
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Anchor for square
from enum import Enum
from typing import List, Dict, Tuple


# Left = 1, Right = 2, Up = 4, Down = 8 (combo involves adding values)
class Anchor(Enum):
    TOPLEFT = 5,
    TOP = 4,
    TOPRIGHT = 6,
    LEFT = 1,
    MID = 0,
    RIGHT = 2,
    BOTLEFT = 9,
    BOT = 8,
    BOTRIGHT = 10

_AnchorValues: Dict[Anchor, Tuple[float, float]] = {
    Anchor.TOPLEFT: [-1, +1],
    Anchor.TOP: [0, +1],
    Anchor.TOPRIGHT: [+1, +1],
    Anchor.LEFT: [-1, 0],
    Anchor.MID: [0, 0],
    Anchor.RIGHT: [+1, 0],
    Anchor.BOTLEFT: [-1, -1],
    Anchor.BOT: [0, -1],
    Anchor.BOTRIGHT: [+1, -1]
}




