

# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Donkey Kong States] -> separated from DonkeyKong.py to help organize

import pygame
import Engine.Input
from Engine.Rigidbody import *
from Engine.Vector import *
from Engine.Clock import *
from enum import Enum


class DK_State_Enum(Enum):
    ERR = 0,
    STILL = 1,
    TOSS_BARREL_NORMAL = 2,
    TOSS_BARREL_SPECIAL = 3


def create_state(dk, new_state: DK_State_Enum):
    if new_state is DK_State_Enum.STILL:
        return DK_State_Still(dk)
    elif new_state is DK_State_Enum.TOSS_BARREL_NORMAL:
        return DK_State_Toss_Barrel_Normal(dk)
    elif new_state is DK_State_Enum.TOSS_BARREL_SPECIAL:
        return DK_State_Toss_Barrel_Special(dk)

    print('unknown donkey kong state')
    return None


class DK_State:
    def __init__(self, _dk):
        self._dk = _dk
        self.ID = DK_State_Enum.ERR
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        pass


class DK_State_Still(DK_State):
    def __init__(self, _dk):
        DK_State.__init__(self, _dk)
        self._timer: Clock = Clock(2.0)
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        pass


class DK_State_Toss_Barrel_Normal(DK_State):
    def __init__(self, _dk):
        DK_State.__init__(self, _dk)
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        pass


class DK_State_Toss_Barrel_Special(DK_State):
    def __init__(self, _dk):
        DK_State.__init__(self, _dk)
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        pass
