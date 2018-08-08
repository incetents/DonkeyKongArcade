
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Mario Character]

from Engine.Entity import *
from Engine.Sprite import *
import Engine.Input
import Engine.Raycast
import pygame
from Game.MarioState import *
import Game.MarioState
# Math
from Engine.Vector import *
# Physics
from Engine.Rigidbody import *
from Engine.Collision import *
from Engine.CollisionManager import *
from Engine.Raycast import *
from Engine.Anchor import *
from Game.Tile import *
import Engine.Config

DEAD_HEIGHT = -10

class Mario(Entity):
    def __init__(self, entity_name: str):
        # Base Constructor
        Entity.__init__(self, entity_name)
        # State
        self._state: MarioState = MarioState_Idle(self)
        # Physics
        self.rigidbody: Rigidbody = self.add_component(Rigidbody(self.transform.get_position()))
        # self.rigidbody = Rigidbody(self.transform.get_position())
        self.rigidbody.set_terminal_velocity_y(250)
        self.rigidbody.set_gravity(Vector3(0, -Engine.Config.GRAV, 0))
        self.collision = self.add_component(Collider_AABB_2D(self.transform.get_position()))
        self.collision.type = Collision_Type.TRIGGER
        self.collision.id = Engine.Config.TRIGGER_ID_MARIO
        self.collision.offset = Vector2(0, 8)
        self._ray_left: Raycast_2D = None
        self._ray_right: Raycast_2D = None
        # Inputs
        self.input_left: bool = False
        self.input_right: bool = False
        self.input_up: bool = False
        self.input_down: bool = False
        self.input_jump: bool = False
        # Animations
        self.animations = SpriteAnimation('anim_mario_idle')
        self.animations.set_speed(8.0)

        # Mario Data
        self.rigid_state_backup: bool = False
        self._debug: bool = False
        self.debug_speed: float = 4
        self.alive: bool = True
        self.speed: float = 35
        self.jumpspeed: float = 50
        self.climbspeed: float = 0.5
        self.x_distance_to_ladder_for_climb: float = 4.0
        self.touching_ground: bool = False
        self._ladder_ref: Tile = None
        self._bottom_left_anchor: Vector2 = Vector2()
        self._bottom_right_anchor: Vector2 = Vector2()

    def set_debug(self, _state: bool):
        # Ignore self change
        if self._debug is _state:
            return

        self._debug = _state
        if _state is True:
            self.rigid_state_backup = self.rigidbody.enabled
        else:
            self.rigidbody.enabled = self.rigid_state_backup

    def set_state(self, _new_state: MarioState_Enum):
        if self._state is not None:
            self._state.exit()

        self._state = Game.MarioState.create_state(self, _new_state)

        if self._state is not None:
            self._state.ID = _new_state
            self._state.enter()

    def set_animation(self, _sequence: str):
        self.animations.set_sprite_sequence(_sequence)

    def update(self, delta_time: float):
        # Debug Mode
        if self._debug:
            self.rigidbody.enabled = False
            self.rigidbody.set_velocity(Vector3(0, 0, 0))
            self.rigidbody.set_gravity(Vector3(0, 0, 0))
            if Engine.Input.get_key(pygame.K_LEFT):
                self.rigidbody.increase_position(Vector3(-self.debug_speed, 0, 0))
            elif Engine.Input.get_key(pygame.K_RIGHT):
                self.rigidbody.increase_position(Vector3(+self.debug_speed, 0, 0))
            if Engine.Input.get_key(pygame.K_UP):
                self.rigidbody.increase_position(Vector3(0, +self.debug_speed, 0))
            elif Engine.Input.get_key(pygame.K_DOWN):
                self.rigidbody.increase_position(Vector3(0, -self.debug_speed, 0))
            return

        # Update Input
        if self.alive is True:
            # Horizontal Movement
            if Engine.Input.get_key(pygame.K_LEFT) and not Engine.Input.get_key(pygame.K_RIGHT):
                self.input_left = True
                self.input_right = False
            elif Engine.Input.get_key(pygame.K_RIGHT) and not Engine.Input.get_key(pygame.K_LEFT):
                self.input_left = False
                self.input_right = True
            else:
                self.input_left = False
                self.input_right = False

            # Vertical Movement
            if Engine.Input.get_key(pygame.K_UP) and not Engine.Input.get_key(pygame.K_DOWN):
                self.input_up = True
                self.input_down = False
            elif Engine.Input.get_key(pygame.K_DOWN) and not Engine.Input.get_key(pygame.K_UP):
                self.input_up = False
                self.input_down = True
            else:
                self.input_up = False
                self.input_down = False

            if Engine.Input.get_key(pygame.K_SPACE):
                self.input_jump = True
            else:
                self.input_jump = False

        # No input
        else:
            self.input_left = False
            self.input_right = False
            self.input_up = False
            self.input_down = False
            self.input_jump = False


        # Update Animations
        self.animations.update(delta_time)
        # self.set_sprite('spr_mario_jump')
        _sprite = self.animations.get_current_frame()

        # Update Physics
        self.collision.set_size_from_sprite(self.transform, _sprite)
        self.rigidbody.set_gravity(Vector3(0, -Engine.Config.GRAV, 0))
        self.rigidbody.update(delta_time)

        self._bottom_left_anchor = _sprite.get_anchor(Anchor.BOTLEFT, self.transform) + Vector2(0, 0.2)
        self._bottom_right_anchor = _sprite.get_anchor(Anchor.BOTRIGHT, self.transform) + Vector2(0, 0.2)

        # Update Raycast Data
        self._ray_left = Raycast_2D(self._bottom_left_anchor, Vector2(0, -1), 5, True)
        self._ray_right = Raycast_2D(self._bottom_right_anchor, Vector2(0, -1), 5, True)

        # Update Ground Data
        self.touching_ground =\
            (self._ray_left.hit_distance < 0.4 and self._ray_left.hit_flag is True) or\
            (self._ray_right.hit_distance < 0.4 and self._ray_right.hit_flag is True)

        # Update State
        self._state.update()

        # Force dead state if below vertical area
        if self.transform.get_position().y < DEAD_HEIGHT and self._state.ID is not MarioState_Enum.DEAD:
            self.set_state(MarioState_Enum.DEAD)

        # Test
        # _cols: List[Entity] = Engine.Raycast.Raypoint_2D(self.transform.get_position().get_vec2())
        # prin# t(len(_cols))

        pass

    def draw(self):
        # Base Draw
        self.animations.draw(self.transform)
        self.collision.draw(Vector3(0, 0, 1))

        # Draw Raycast Stuff
        Debug.draw_circle_2d( self._bottom_left_anchor, 1.0, Vector3(0, 1, 0))
        Debug.draw_circle_2d(self._bottom_right_anchor, 1.0, Vector3(0, 1, 0))

        if self._ray_left is not None and self._ray_right is not None:
            Debug.draw_line_2d(
                self._bottom_left_anchor,
                self._ray_left.ray_end,
                Vector3(1, 0, 0)
            )
            Debug.draw_line_2d(
                self._bottom_right_anchor,
                self._ray_right.ray_end,
                Vector3(1, 0, 0)
            )

            if self._ray_left.hit_flag is not False:
                Debug.draw_circle_2d(self._ray_left.hit_point, 2.0, Vector3(0,1,0))
            if self._ray_right.hit_flag is not False:
                Debug.draw_circle_2d(self._ray_right.hit_point, 2.0, Vector3(0,1,0))

    def trigger_stay(self, trigger: Collider):
        pass

    def trigger_enter(self, trigger: Collider):
        # Death Trigger
        if self._debug is False and trigger.id is Engine.Config.TRIGGER_ID_DEATH:
            self.set_state(MarioState_Enum.DEAD)

        # Ladder Exception
        if self._debug is False and trigger.id is Engine.Config.TRIGGER_ID_BARREL and \
                self._state.ID is MarioState_Enum.CLIMB:
            self.set_state(MarioState_Enum.DEAD)

        # Hold copy of ladder
        # if trigger.id is Engine.Config.TRIGGER_ID_LADDER:
        #     self.ladder_ref = trigger.entity_parent

        # print('ENTER id:', trigger.id)
        pass

    def trigger_exit(self, trigger: Collider):
        # Lose copy of ladder
        # if trigger.id is Engine.Config.TRIGGER_ID_LADDER and \
        #         self.ladder_ref is trigger.entity_parent and \
        #         self._state.ID is not MarioState_Enum.CLIMB:
        #     self.ladder_ref = None

        # print('EXIT id:', trigger.id)
        pass


