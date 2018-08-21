

# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Donkey Kong States] -> separated from DonkeyKong.py to help organize

from enum import Enum
import pygame
import Engine.Input
from Engine.Rigidbody import *
from Engine.Vector import *
from Engine.Clock import *
from Game.Barrel import *


class DK_State_Enum(Enum):
    NONE = 0,
    STILL = 1,
    TOSS_BARREL_RIGHT = 2,
    TOSS_BARREL_DROP = 3


def create_state(dk, new_state: DK_State_Enum):
    if new_state is DK_State_Enum.STILL:
        return DK_State_Still(dk)
    elif new_state is DK_State_Enum.TOSS_BARREL_RIGHT:
        return DK_State_Toss_Barrel_Right(dk)
    elif new_state is DK_State_Enum.TOSS_BARREL_DROP:
        return DK_State_Toss_Barrel_Drop(dk)

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
        self.timer: Clock = Clock(0.5)
        pass

    def enter(self):
        self._dk.set_frame(0)
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        if self.timer.is_finished():
            _count: int = self._dk.get_total_barrel_count()
            # First barrel is drop / or every 7th barrel
            if _count % 7 is 0:
                self._dk.set_state(DK_State_Enum.TOSS_BARREL_DROP)
            else:
                self._dk.set_state(DK_State_Enum.TOSS_BARREL_RIGHT)
        pass


class DK_State_Toss_Barrel_Right(DK_State):
    def __init__(self, _dk):
        DK_State.__init__(self, _dk)
        self.id = DK_State_Enum.TOSS_BARREL_RIGHT
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
                self._dk.spawn_barrel(_state=Barrel_State.RIGHT)
                self.spawned = True
        elif self.clocks[0].is_finished():
            self._dk.set_frame(3)
        else:
            self._dk.set_frame(1)
        pass


class DK_State_Toss_Barrel_Drop(DK_State):
    def __init__(self, _dk):
        DK_State.__init__(self, _dk)
        self.id = DK_State_Enum.TOSS_BARREL_DROP
        self.clocks: List[Clock] = (Clock(0.5), Clock(1.0), Clock(1.5))
        # Left, hold barrel, drop, (return to still)
        self.spawned: bool = False
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        import Game.GameData
        # print('drop mode')
        if self.clocks[2].is_finished():
            self._dk.set_state(DK_State_Enum.STILL)
        elif self.clocks[1].is_finished():
            self._dk.set_frame(5)
            if self.spawned is False:
                # blue if first
                blue: bool = (self._dk.get_total_barrel_count() is 0)
                # check if level 1
                level_num: int = Game.GameData.level_id_check
                if level_num is 1:
                    self._dk.spawn_barrel(_state=Barrel_State.MEGA_FALL, _blue=blue)
                else:
                    self._dk.spawn_barrel(_state=Barrel_State.MEGA_FALL_RIGHT, _blue=blue)

                self.spawned = True
        elif self.clocks[0].is_finished():
            # blue if first
            blue: bool = (self._dk.get_total_barrel_count() is 0)
            if blue:
                self._dk.set_frame(4)
            else:
                self._dk.set_frame(3)
        else:
            self._dk.set_frame(1)
        pass
