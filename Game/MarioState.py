
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Mario Character States] -> separated from Mario.py to help organize

import pygame
import Engine.Input
from Engine.Rigidbody import *
from Engine.Vector import *
from Engine.Clock import *
from enum import Enum
from Engine.Collision import *
from Engine.Raycast import *
from Game.Tile import *
import Engine.Raycast
from random import randint

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
        self._mario.animations.set_pause(False)
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
        self._mario.rigidbody.set_gravity_state(True)
        self._mario.rigidbody.ignore_static_colliders = False
        self._mario.set_animation('anim_mario_idle')
        self._mario.animations.set_pause(False)
        pass

    def exit(self):
        pass

    def update(self):
        # No movement
        self._mario.rigidbody.set_vel_x(0)

        # Update Flip
        if self._mario.input_left:
            self._mario.transform.set_flip_x(False)
        elif self._mario.input_right:
            self._mario.transform.set_flip_x(True)

        # Movement Change
        if self._mario.input_left or self._mario.input_right:
            self._mario.set_state(MarioState_Enum.WALK)

        elif self._mario.input_jump and self._mario.touching_ground:
            self._mario.set_state(MarioState_Enum.JUMP)

        # Climb Up
        if self._mario.input_up and self._mario.touching_ground:
            # Raypoint at mario center
            _ents: List[Entity] = Engine.Raycast.Raypoint_2D_Static(
                self._mario.collision.get_position().get_vec2(),
                Engine.Config.TRIGGER_ID_LADDER
            )
            for e in _ents:
                # Get ladder if exists
                _ladder_collision: Collider_AABB_2D = e.get_component(Collider_AABB_2D)
                if _ladder_collision is not None and _ladder_collision.id is Engine.Config.TRIGGER_ID_LADDER:
                    # Set Mario Position
                    self._mario.transform.set_position_x(_ladder_collision.get_position().x)
                    # Set ladder ref
                    self._mario._ladder_ref = e
                    # Set State
                    self._mario.set_state(MarioState_Enum.CLIMB)

        # Climb Down
        elif self._mario.input_down and self._mario.touching_ground:
            # Raypoint below mario (16 units below)
            _ents: List[Entity] = Engine.Raycast.Raypoint_2D_Static(
                self._mario.transform.get_position().get_vec2() + Vector2(0, -Engine.Config.TILE_SIZE - 2.0),
                Engine.Config.TRIGGER_ID_LADDER
            )
            for e in _ents:
                # Get ladder if exists
                _ladder_collision: Collider_AABB_2D = e.get_component(Collider_AABB_2D)
                if _ladder_collision is not None and _ladder_collision.id is Engine.Config.TRIGGER_ID_LADDER:

                    # if close enough to ladder ( 2 checks )
                    _collide1 = _ladder_collision.check_if_point_inside(
                        self._mario.transform.get_position().get_vec2() + Vector2(0, -2)
                    )
                    _collide2 = _ladder_collision.check_if_point_inside(
                        self._mario.transform.get_position().get_vec2() + Vector2(0, -(2 + Engine.Config.TILE_SIZE))
                    )

                    # if collide with either point, teleport to top of ladder and set to climb state
                    if _collide1 or _collide2:
                        # Set position
                        self._mario.transform.set_position_x(_ladder_collision.get_position().x)
                        if _collide1:
                            self._mario.transform.set_position_y(_ladder_collision.get_up())
                        elif _collide2:
                            self._mario.transform.set_position_y(_ladder_collision.get_up() + Engine.Config.TILE_SIZE - 2)
                        # Set ladder ref
                        self._mario._ladder_ref = e
                        # Set State
                        self._mario.set_state(MarioState_Enum.CLIMB)

        pass


class MarioState_Walk(MarioState):
    def __init__(self, _mario):
        MarioState.__init__(self, _mario)
        # Audio
        self.walk_sfx_clock: Clock = Clock(0.18)
        pass

    def enter(self):
        self._mario.rigidbody.set_gravity_state(True)
        self._mario.rigidbody.ignore_static_colliders = False
        self._mario.set_animation('anim_mario_walk')
        self._mario.animations.set_pause(False)
        # self.walk_sfx_clock.finish()
        pass

    def exit(self):
        pass

    def update(self):
        # Update Flip
        if self._mario.input_left:
            self._mario.transform.set_flip_x(False)
        elif self._mario.input_right:
            self._mario.transform.set_flip_x(True)

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

        # Audio
        if self.walk_sfx_clock.is_finished():
            self._mario.get_random_walk_sfx().play()
            self.walk_sfx_clock.reset()

        pass


class MarioState_Jump(MarioState):
    def __init__(self, _mario):
        MarioState.__init__(self, _mario)
        pass

    def enter(self):
        self._mario.rigidbody.set_gravity_state(True)
        self._mario.rigidbody.ignore_static_colliders = False
        self._mario.set_animation('anim_mario_jump')
        self._mario.animations.set_pause(False)
        self._mario.rigidbody.set_vel_y(self._mario.jumpspeed)
        self._mario.rigidbody.increase_position(Vector3(0, 1, 0))
        # Audio
        self._mario.sfx_jump.play()
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
        self.ladder_top_has_block: bool = False
        self.ladder_bot: float = self._mario._ladder_ref.collision.get_down()
        self.ladder_top: float = self._mario._ladder_ref.collision.get_up()
        self.can_exit_down: bool = True
        # Audio
        self.walk_sfx_clock: Clock = Clock(0.35)

        # Check for additional block
        _ents: List[Entity] = Engine.Raycast.Raypoint_2D_Static(Vector2(
            self._mario._ladder_ref.collision.get_position().x,
            self._mario._ladder_ref.collision.get_up() + Engine.Config.TILE_SIZE - 2.0
            ),
            Engine.Config.TRIGGER_ID_FLOOR
        )
        for e in _ents:
            if e.collision.type is Collision_Type.PLATFORM:
                self.ladder_top_has_block: bool = True
                self.ladder_top += Engine.Config.TILE_SIZE
                break

        # If floating top portion of a ladder, add additional slack
        _ents: List[Entity] = Engine.Raycast.Raypoint_2D_Static(Vector2(
            self._mario._ladder_ref.collision.get_position().x,
            self._mario._ladder_ref.collision.get_down() - 2.0
        ),
            Engine.Config.TRIGGER_ID_FLOOR
        )
        _nothing_below_ladder: bool = True
        for e in _ents:
            if e.collision.type is Collision_Type.PLATFORM:
                _nothing_below_ladder = False
                break
        if _nothing_below_ladder:
            self.can_exit_down = False
            self.ladder_bot -= Engine.Config.TILE_SIZE
        pass

    def enter(self):
        self._mario.rigidbody.set_gravity_state(False)
        self._mario.rigidbody.ignore_static_colliders = True
        self._mario.rigidbody.set_velocity(Vector3())
        self._mario.set_animation('anim_mario_climb')
        self._mario.animations.set_pause(True)
        pass

    def exit(self):
        pass

    def update(self):
        # Audio
        if self._mario.input_down or self._mario.input_up:
            # Audio
            if self.walk_sfx_clock.is_finished():
                self._mario.get_random_walk_sfx().play()
                self.walk_sfx_clock.reset()

        # Movement
        if self._mario.input_up:
            self._mario.transform.increase_position(Vector3(0, +self._mario.climbspeed, 0))
            # if reached top of ladder, go to idle
            if self._mario.transform.get_position().y > self.ladder_top:
                self._mario.set_state(MarioState_Enum.IDLE)

        elif self._mario.input_down:
            self._mario.transform.increase_position(Vector3(0, -self._mario.climbspeed, 0))
            # if touching ground, go to idle
            if self.can_exit_down:
                if self._mario.transform.get_position().y < self.ladder_bot:
                    self._mario.set_state(MarioState_Enum.IDLE)
            else:
                _y_fix: float = max(self._mario.transform.get_position().y, self.ladder_bot)
                self._mario.transform.set_position_y(_y_fix)

        # Set Animation State based on y position
        _frame = math.floor(self._mario.transform.get_position().y / 4.0) % 2
        _dist_to_top: float = abs(self.ladder_top - self._mario.transform.get_position().y)

        if _dist_to_top < 3.0:
            _frame = 4
        elif _dist_to_top < 5.0:
            _frame = 0
        elif _dist_to_top < 7.0:
            _frame = 3
        elif _dist_to_top < 9.0:
            _frame = 2

        self._mario.animations.set_frame(_frame)

        pass