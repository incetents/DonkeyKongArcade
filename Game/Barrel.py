
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Barrel has a bit of complexity,
# can be moving left or right normally, go down ladders
# or it can fall from its spawn position from donkey kong

from __future__ import annotations
from Engine.Entity import *
from Engine.EntityManager import *
from Engine.Sprite import *
import pygame
from Game.MarioState import *
import Game.MarioState
from Game.Direction import *
# Math
from Engine.Vector import *
from Engine.Raycast import *
from Engine.Config import *
# Physics
from Engine.Rigidbody import *
from Engine.Collision import *
import Engine.Raycast
import Engine.Collision
import Engine.Config
from Game.Oilbarrel import *
from enum import Enum
from random import randint
import Engine.Storage

oil_barrel_ref: Oilbarrel = None
mario_ref: Mario = None


class BarrelScore(Entity):
    def __init__(self, entity_name: str, _position: Vector3, _sprite_name: str):
        # Base Constructor
        Entity.__init__(self, entity_name)
        self.transform.set_position(_position)
        # Animations
        self.animations = SpriteAnimation('anim_enemy1')
        self.animations.set_speed(10.0)

        # Sprite
        self.sprite: Sprite = Engine.Storage.get(Engine.Storage.Type.SPRITE, _sprite_name)
        # Data
        self.time: Clock = Clock(1.0)

    def update(self, delta_time):
        if self.time.is_finished():
            EntityManager.get_singleton().remove_entity(self)
        pass

    def draw(self):
        if self.sprite is not None:
            self.sprite.draw(self.transform)
        pass


class BarrelZone(Entity):
    def __init__(self, trigger_name: str, barrel: Barrel):
        # Base
        Entity.__init__(self, trigger_name)
        self._barrel = barrel
        self.transform.set_position(barrel.transform.get_position())
        # Physics
        self.rigidbody = self.add_component(Rigidbody(self.transform.get_position()))
        self.rigidbody.ignore_dynamic_colliders = True
        self.collision: Collider_AABB_2D = self.add_component(Collider_AABB_2D(self.transform.get_position()))
        self.collision.size = Vector2(4, 20)
        self.collision.offset = Vector2(0, 10)
        self.collision.type = Collision_Type.TRIGGER
        self.collision.id = Engine.Config.TRIGGER_ID_BARREL_SPECIAL

    def update(self, delta_time):
        if self._barrel.deleted:
            EntityManager.get_singleton().remove_entity(self)
        else:
            self.transform.set_position(self._barrel.transform.get_position())
            self.rigidbody.update(delta_time)
        pass

    def draw(self):
        self.collision.draw(Vector3(0, 1, 0.5))
        Debug.draw_line_2d(
            self.collision.get_position().get_vec2() + Vector2(-8, -2),
            self.collision.get_position().get_vec2() + Vector2(+8, -2),
            Vector3(0.75,0.75,0)
        )


class Barrel_State(Enum):
    LEFT = 1,
    RIGHT = 2,
    LADDER_LEFT = 3,
    LADDER_RIGHT = 4,
    MEGA_FALL = 5,
    MEGA_FALL_RIGHT = 6


class Barrel(Entity):
    def __init__(self, entity_name: str, _pos: Vector3,
                 _state: Barrel_State = Barrel_State.RIGHT, _blue: bool=False):
        # Base Constructor
        Entity.__init__(self, entity_name)
        self.transform.set_position(_pos)
        # Physics
        self.rigidbody: Rigidbody = self.add_component(Rigidbody(self.transform.get_position()))
        self.rigidbody.set_terminal_velocity_y(250)
        self.rigidbody.set_gravity(Vector3(0, -120, 0))
        self.rigidbody.ignore_dynamic_colliders = True
        # self.rigidbody.enabled = False
        self.collision = self.add_component(Collider_AABB_2D(self.transform.get_position()))
        self.collision.offset = Vector2(0, 5)
        self.collision.type = Collision_Type.TRIGGER
        self.collision.id = Engine.Config.TRIGGER_ID_BARREL
        self._ray_left: Raycast_2D = None
        self._ray_right: Raycast_2D = None
        # Animations
        self.animations = SpriteAnimation('anim_barrel_roll')
        self.animations.set_speed(8.0)

        # Data
        self._blue_mode: bool = _blue
        self.h_speed_current: float = 0
        self.h_speed_move: float = 55
        self.h_speed_fall: float = 20
        self.v_speed_fall: float = 30
        self.v_speed_ladder: float = 45
        self.mega_fall_right_speed: float = 30
        self._state: Barrel_State = _state
        self.update_visual()

        self.fall_clock = Clock(0.5)

    def update_visual(self):
        if self._state is Barrel_State.LADDER_LEFT or \
                self._state is Barrel_State.LADDER_RIGHT or \
                self._state is Barrel_State.MEGA_FALL or\
                self._state is Barrel_State.MEGA_FALL_RIGHT:
            # FALLING
            if self._blue_mode:
                self.animations.set_sprite_sequence('anim_barrel_fall_blue')
            else:
                self.animations.set_sprite_sequence('anim_barrel_fall')
        else:
            # MOVING LEFT OR RIGHT
            if self._blue_mode:
                self.animations.set_sprite_sequence('anim_barrel_roll_blue')
            else:
                self.animations.set_sprite_sequence('anim_barrel_roll')

    def check_use_ladder(self) -> Tile:
        # Acquire Ladder Below Barrel
        _ents = Engine.Raycast.Raypoint_2D_Static(
            self.transform.get_position().get_vec2() + Vector2(0, -Engine.Config.TILE_SIZE - 2.0),
            Engine.Config.TRIGGER_ID_LADDER
        )

        # Ignore if no entities are found
        if len(_ents) is 0:
            return None

        # Ladder
        _ladder_ref: Tile = _ents[0]

        # Ignore if ladder is too far away
        if abs(self.transform.get_position().x - _ladder_ref.transform.get_position().x) > 2.0:
            return None

        global oil_barrel_ref
        if not oil_barrel_ref.check_lit():
            return _ladder_ref

        # If mario is above barrel, never go done ladder
        if mario_ref.transform.get_position().y > self.transform.get_position().y:
            return None

        # Random variable on whether or not barrel should go down
        _difficulty_value = 2
        _r1: int = randint(0, 255)  # get random number from 0 to 255 (inclusive)
        _r2 = _r1 % 3               # get random number from 0 to 3 (inclusive)
        if _r2 >= ((_difficulty_value % 2) + 1):
            return None

        # !!!!!!!!!!!!!!!!
        _barrel_x: float = self.transform.get_position().x
        _mario_x: float = mario_ref.transform.get_position().x
        _mario_rigidbody: Rigidbody = mario_ref.get_component(Rigidbody)

        # If barrel is directly above Mario, go down
        if abs(_barrel_x - _mario_x) < 5.0:
            return _ladder_ref

        # Barrel is left of mario and he's moving left
        if _barrel_x < _mario_x and _mario_rigidbody.get_velocity().x < 0:
            return _ladder_ref

        # Barrel is right of mario and he's moving left
        if _barrel_x > _mario_x and _mario_rigidbody.get_velocity().x > 0:
            return _ladder_ref

        # 75% chance to return without ladder
        if (_r1 & 0x18) is not 0:
            return None
        # 25% chance to return with ladder
        return _ladder_ref

    def update(self, delta_time):
        # Set State based on direction
        _sprite = self.animations.get_current_frame()

        # Update Physics
        self.collision.set_size_from_sprite(self.transform, _sprite)
        self.rigidbody.update(delta_time)

        # Raycast to see if anything below barrel
        self._bottom_left_anchor = _sprite.get_anchor(Anchor.BOTLEFT, self.transform) + Vector2(0, 0.2)
        self._bottom_right_anchor = _sprite.get_anchor(Anchor.BOTRIGHT, self.transform) + Vector2(0, 0.2)

        # print('~~~')#
        # _t = pygame.time.get_ticks()
        self._ray_left = Raycast_2D(self._bottom_left_anchor, Vector2(0, -1), 5, True)
        self._ray_right = Raycast_2D(self._bottom_right_anchor, Vector2(0, -1), 5, True)
        # print('raycast time for:', self.name, pygame.time.get_ticks() - _t)

        # Update Ground Data
        self.above_emptiness = \
            (self._ray_left.hit_distance > 1.25 or self._ray_left.hit_flag is False) and \
            (self._ray_right.hit_distance > 1.25 or self._ray_right.hit_flag is False)

        if self.above_emptiness is True:
            self.h_speed_current = self.h_speed_fall
        else:
            self.h_speed_current = self.h_speed_move

        # Ladder possiblity if moving left or right
        if (self._state is Barrel_State.LEFT or self._state is Barrel_State.RIGHT) and \
            self.above_emptiness is False:
            #
            _ladder = self.check_use_ladder()
            if _ladder is not None:
                # Move barrel to top of ladder
                self.transform.set_position_x(_ladder.collision.get_position().x)
                self.transform.set_position_y(_ladder.collision.get_up() + Engine.Config.TILE_SIZE/2)
                self.fall_clock.reset()
                if self._state is Barrel_State.LEFT:
                    self._state = Barrel_State.LADDER_RIGHT
                else:
                    self._state = Barrel_State.LADDER_LEFT
                self.update_visual()

        # Move Left
        if self._state is Barrel_State.LEFT:
            self.animations.update(-delta_time * (0.0 if self.above_emptiness is True else 1.0))
            self.rigidbody.ignore_static_colliders = False
            self.rigidbody.set_vel_x(-self.h_speed_current)
            self.rigidbody.set_gravity_state(True)
        # Move Right
        elif self._state is Barrel_State.RIGHT:
            self.animations.update(+delta_time * (0.0 if self.above_emptiness is True else 1.0))
            self.rigidbody.ignore_static_colliders = False
            self.rigidbody.set_vel_x(+self.h_speed_current)
            self.rigidbody.set_gravity_state(True)
        # Move Down ladder
        elif self._state is Barrel_State.LADDER_LEFT or self._state is Barrel_State.LADDER_RIGHT:
            # Animation
            self.animations.update(delta_time)

            # Ignore static colliders until clock reaches end
            self.rigidbody.ignore_static_colliders = not self.fall_clock.is_finished()
            self.rigidbody.set_gravity_state(False)
            self.rigidbody.set_vel_x(0)
            self.rigidbody.set_vel_y(-self.v_speed_ladder)

            # Check if barrel reaches floor
            if self.fall_clock.is_finished() and not self.above_emptiness:
                if self._state is Barrel_State.LADDER_LEFT:
                    self._state = Barrel_State.LEFT
                else:
                    self._state = Barrel_State.RIGHT
                self.update_visual()

        # Fall Down to lowest floor
        elif self._state is Barrel_State.MEGA_FALL or self._state is Barrel_State.MEGA_FALL_RIGHT:
            self.animations.update(delta_time)

            # Grav flag
            self.rigidbody.set_gravity_state(True)

            # Movement possibility
            if self.above_emptiness and self._state is Barrel_State.MEGA_FALL_RIGHT:
                self.rigidbody.set_vel_x(+self.mega_fall_right_speed)

            # Ignore static colliders until clock reaches end
            self.rigidbody.ignore_static_colliders = not self.fall_clock.is_finished()

            # If reached bottom of map, turn into left moving barrel
            if self.transform.get_position().y < 16.0 and not self.above_emptiness:
                self._state = Barrel_State.LEFT
                self.rigidbody.set_vel_y(0)
                self.update_visual()

            # Check at barrel bottom if its hitting a floor
            elif self.fall_clock.is_finished() and not self.above_emptiness:
                self.fall_clock.reset()
                self.rigidbody.set_vel_y(0)


    def draw(self):
        self.animations.draw(self.transform)
        self.collision.draw(Vector3(1, 0, 0))

        Debug.draw_x_2d(
            self.transform.get_position().get_vec2() + Vector2(0, -Engine.Config.TILE_SIZE - 2.0),
            5.0, Vector3(1, 0, 1)
        )

        # Draw Raycast Stuff
        # if self._ray_right is not None and self._ray_left is not None:
        #     Debug.draw_circle_2d(self._bottom_left_anchor, 1.0, Vector3(0, 1, 0))
        #     Debug.draw_circle_2d(self._bottom_right_anchor, 1.0, Vector3(0, 1, 0))
        #     Debug.draw_line_2d(
        #         self._bottom_left_anchor,
        #         self._ray_left.ray_end,
        #         Vector3(1, 0, 0)
        #     )
        #     Debug.draw_line_2d(
        #         self._bottom_right_anchor,
        #         self._ray_right.ray_end,
        #         Vector3(1, 0, 0)
        #     )
        #     if self._ray_left.hit_flag is not False:
        #         Debug.draw_circle_2d(self._ray_left.hit_point, 2.0, Vector3(0,1,0))
        #     if self._ray_right.hit_flag is not False:
        #         Debug.draw_circle_2d(self._ray_right.hit_point, 2.0, Vector3(0,1,0))

    def collider_enter(self, collider: Collider):
        # hitting walls on the edge of map
        if collider.id is Engine.Config.TRIGGER_ID_WALL:
            if self._state is Barrel_State.RIGHT:
                self._state = Barrel_State.LEFT
            else:
                self._state = Barrel_State.RIGHT

    def trigger_enter(self, trigger: Collider):
        # Spawn fire when hit oil barrel
        if trigger.id is Engine.Config.TRIGGER_ID_OIL_BARREL:
            _oil: Oilbarrel = trigger.entity_parent
            _oil.spawn_fire()
        # Destroy self if hit death trigger
        elif trigger.id is Engine.Config.TRIGGER_ID_BARREL_DESTROY:
            EntityManager.get_singleton().remove_entity(self)

        pass