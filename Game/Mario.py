
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Mario Character]

from Engine.Entity import *
from Engine.Sprite import *
import Engine.Input
import pygame
from Game.MarioState import *
import Game.MarioState
# Math
from Engine.Vector import *
# Physics
from Engine.Rigidbody import *
from Engine.Collision import *
import Engine.Config

DEAD_HEIGHT = -10

class Mario(Entity_2D):
    def __init__(self, entity_name: str):
        # Base Constructor
        Entity_2D.__init__(self, entity_name)
        # State
        self._state: MarioState = MarioState_Idle(self)
        # Physics
        self.rigidbody = Rigidbody(self.transform.get_position())
        self.rigidbody.set_terminal_velocity_y(250)
        self.rigidbody.set_gravity(Vector3(0, -100, 0))
        self.collision = Collider_AABB_2D(self.transform.get_position())
        # Inputs
        self.input_left: bool = False
        self.input_right: bool = False
        self.input_jump: bool = False
        # Animations
        self.animations = SpriteAnimation('anim_mario_idle')
        self.animations.set_speed(8.0)

        # Mario Data
        self.alive = True
        self.speed = 35
        self.jumpspeed = 50

    def set_state(self, _new_state: MarioState_Enum):
        self._state.exit()
        self._state = Game.MarioState.create_state(self, _new_state)
        self._state.ID = _new_state
        self._state.enter()

    def set_animation(self, _sequence: str):
        self.animations.set_sprite_sequence(_sequence)

    def update(self, delta_time: float):
        # Update Input
        if self.alive is True:
            if Engine.Input.get_key(pygame.K_LEFT) and not Engine.Input.get_key(pygame.K_RIGHT):
                self.input_left = True
                self.input_right = False
                self.transform.set_flip_x(False)
            elif Engine.Input.get_key(pygame.K_RIGHT) and not Engine.Input.get_key(pygame.K_LEFT):
                self.input_left = False
                self.input_right = True
                self.transform.set_flip_x(True)
            else:
                self.input_left = False
                self.input_right = False

            if Engine.Input.get_key(pygame.K_SPACE) or Engine.Input.get_key(pygame.K_UP):
                self.input_jump = True
            else:
                self.input_jump = False

        # Update Animations
        self.animations.update(delta_time)
        # self.set_sprite('spr_mario_jump')
        _sprite = self.animations.get_current_frame()

        # Update Physics
        self.collision.update_size_from_sprite(self.transform, _sprite)
        self.rigidbody.update(delta_time)

        # Update State
        self._state.update()
        # Force dead state if below vertical area
        if self.transform.get_position().y < DEAD_HEIGHT and self._state.ID is not MarioState_Enum.DEAD:
            self.set_state(MarioState_Enum.DEAD)

        pass

    def draw(self):
        # Base Draw
        self.animations.draw(self.transform)
        self.collision.draw(Vector3(0, 0, 1))

    def col_collider_stay(self, collider: Collider):
        pass

    def col_collider_enter(self, collider: Collider):
        pass

    def col_collider_exit(self, collider: Collider):
        pass

    def col_trigger_stay(self, trigger: Collider):
        # print('trigger id:', trigger.id)
        pass

    def col_trigger_enter(self, trigger: Collider):
        if trigger.id is Engine.Config.TRIGGER_ID_DEATH:
            self.set_state(MarioState_Enum.DEAD)
        print('ENTER id:', trigger.id)
        pass

    def col_trigger_exit(self, trigger: Collider):
        print('EXIT id:', trigger.id)
        pass


