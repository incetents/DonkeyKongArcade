
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# DK from stage 1 that randomly throws barrels at given intervals

from Engine.Entity import *
from Engine.Sprite import *
import pygame
from enum import Enum
from Game.MarioState import *
import Game.MarioState
from Game.Direction import *
# Math
from Engine.Vector import *
from Engine.Raycast import *
from Engine.Config import *
from Engine.Clock import *
# Physics
from Engine.Rigidbody import *
from Engine.Collision import *
import Engine.Config
from Game.DonkeyKongState import *
import Game.DonkeyKongState


class DonkeyKong(Entity_2D):
    def __init__(self, entity_name: str, _pos: Vector3):
        # Base Constructor
        Entity_2D.__init__(self, entity_name)
        self.transform.set_position(_pos)

        # Physics
        self.collision = Collider_AABB_2D(self.transform.get_position())
        self.collision.offset = Vector2(0, 16)
        self.collision.type = Collision_Type.TRIGGER
        self.collision.id = Engine.Config.TRIGGER_ID_DEATH
        self.collision.size = Vector2(40, 32)
        # Animations
        self.animations = SpriteAnimation('anim_dk_frames')
        self.animations.set_speed(4.0)

        # Data
        self._state: DK_State = None

    def set_state(self, _new_state: DK_State_Enum):
        if self._state is not None:
            self._state.exit()

        self._state = Game.DonkeyKongState.create_state(self, _new_state)

        if self._state is not None:
            self._state.ID = _new_state
            self._state.enter()

    def update(self, delta_time):
        self.animations.update(delta_time)
        _sprite = self.animations.get_current_frame()

        # # Simple AI
        # if self._state is DK_Barrel_State.STILL:
        #     # If time is complete
        #     if self._timer.is_finished():
        #         self._state = DK_Barrel_State.THROW

        # Update Physics



    def draw(self):
        self.animations.draw(self.transform)
        self.collision.draw(Vector3(1, 0, 0))

# SpriteSequence('anim_dk_frames',
#                        'spr_dk_center',
#                        'spr_dk_left',
#                        'spr_dk_right',
#                        'spr_dk_hold_barrel1',
#                        'spr_dk_hold_barrel2',
#                        'spr_dk_drop'
#                        )

