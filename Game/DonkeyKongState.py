

# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Donkey Kong States] -> separated from DonkeyKong.py to help organize

import pygame
import Engine.Input
from Engine.Rigidbody import *
from Engine.Vector import *
from Engine.Clock import *
from enum import Enum


class DK_State_Enum(Enum):
    NONE = 0,
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
        self.id = DK_State_Enum.NONE
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
        self.id = DK_State_Enum.STILL
        self.timer: Clock = Clock(2.0)
        pass

    def enter(self):
        self._dk.set_frame(0)
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        # print(self.timer.get_remaining_time())
        # if self.timer.is_finished():
        #     self._dk.set_state(DK_State_Enum.TOSS_BARREL_NORMAL)
        pass


class DK_State_Toss_Barrel_Normal(DK_State):
    def __init__(self, _dk):
        DK_State.__init__(self, _dk)
        self.id = DK_State_Enum.TOSS_BARREL_NORMAL
        self.clocks: List[Clock] = (Clock(0.5), Clock(1.0), Clock(1.5))
        # Left, hold barrel, Right, (return to still)
        self.spawned: bool = False
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        # print('toss mode')
        if self.clocks[2].is_finished():
            self._dk.set_state(DK_State_Enum.STILL)
        elif self.clocks[1].is_finished():
            self._dk.set_frame(2)
            if self.spawned is False:
                self._dk.spawn_barrel()
                self.spawned = True
        elif self.clocks[0].is_finished():
            self._dk.set_frame(3)
        else:
            self._dk.set_frame(1)
        pass


class DK_State_Toss_Barrel_Special(DK_State):
    def __init__(self, _dk):
        DK_State.__init__(self, _dk)
        self.id = DK_State_Enum.TOSS_BARREL_SPECIAL
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        pass
