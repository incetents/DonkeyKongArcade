
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Mario Character States] -> separated from Mario.py to help organize

import pygame
import Engine.Input
from Engine.Rigidbody import *
from Engine.Vector import *
from Engine.Clock import *
from enum import Enum

class MarioState_Enum(Enum):
    ERR = 0,
    IDLE = 1,
    WALK = 2,
    JUMP = 3,
    DEAD = 4,
    CLIMB = 5


def create_state(mario, new_state: MarioState_Enum):
    if new_state is MarioState_Enum.IDLE:
        return MarioState_Idle(mario)
    elif new_state is MarioState_Enum.WALK:
        return MarioState_Walk(mario)
    elif new_state is MarioState_Enum.JUMP:
        return MarioState_Jump(mario)
    elif new_state is MarioState_Enum.DEAD:
        return MarioState_Dead(mario)
    elif new_state is MarioState_Enum.CLIMB:
        return MarioState_Climb(mario)

    print('unknown mario state')
    return None


class MarioState:
    def __init__(self, _mario):
        self._mario = _mario
        self.ID = MarioState_Enum.ERR
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self):
        pass


class MarioState_Dead(MarioState):
    def __init__(self, _mario):
        MarioState.__init__(self, _mario)
        self._dead1_clock = Clock(1.2)
        self._dead2_clock = Clock(3.0)
        pass

    def enter(self):
        self._mario.set_animation('anim_mario_dying')
        self._mario.rigidbody.enabled = False
        self._mario.alive = False
        pass

    def exit(self):
        pass

    def update(self):
        if self._dead1_clock.is_finished():
            self._mario.set_animation('anim_mario_dead')
        if self._dead2_clock.is_finished():
            pass


class MarioState_Idle(MarioState):
    def __init__(self, _mario):
        MarioState.__init__(self, _mario)
        pass

    def enter(self):
        self._mario.set_animation('anim_mario_idle')
        pass

    def exit(self):
        pass

    def update(self):
        # No movement
        self._mario.rigidbody.set_vel_x(0)

        # Movement Change
        if self._mario.input_left or self._mario.input_right:
            self._mario.set_state(MarioState_Enum.WALK)

        elif self._mario.input_jump and self._mario.touching_ground is True:
            self._mario.set_state(MarioState_Enum.JUMP)
        #
        pass


class MarioState_Walk(MarioState):
    def __init__(self, _mario):
        MarioState.__init__(self, _mario)
        pass

    def enter(self):
        self._mario.set_animation('anim_mario_walk')
        pass

    def exit(self):
        pass

    def update(self):
        # Movement
        if self._mario.input_left:
            self._mario.rigidbody.set_vel_x(-self._mario.speed)

        elif self._mario.input_right:
            self._mario.rigidbody.set_vel_x(+self._mario.speed)

        # Stop Movement
        if not self._mario.input_left and not self._mario.input_right:
            self._mario.set_state(MarioState_Enum.IDLE)

        elif self._mario.input_jump and self._mario.touching_ground is True:
            self._mario.set_state(MarioState_Enum.JUMP)
        pass


class MarioState_Jump(MarioState):
    def __init__(self, _mario):
        MarioState.__init__(self, _mario)
        pass

    def enter(self):
        self._mario.set_animation('anim_mario_jump')

        self._mario.rigidbody.set_vel_y(self._mario.jumpspeed)
        self._mario.rigidbody.increase_position(Vector3(0, 1, 0))
        pass

    def exit(self):
        pass

    def update(self):
        # Movement
        if self._mario.input_left:
            self._mario.rigidbody.set_vel_x(-self._mario.speed)

        elif self._mario.input_right:
            self._mario.rigidbody.set_vel_x(+self._mario.speed)

        else:
            self._mario.rigidbody.set_vel_x(0)

        if self._mario.touching_ground is True:
            self._mario.set_state(MarioState_Enum.IDLE)
        pass


class MarioState_Climb(MarioState):
    def __init__(self, _mario):
        MarioState.__init__(self, _mario)
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self):
        pass