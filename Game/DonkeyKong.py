
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# DK from stage 1 that randomly throws barrels at given intervals

from Engine.Entity import *
from Engine.EntityManager import *
from Engine.Sprite import *
import pygame
from enum import Enum
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
from Game.Barrel import *
import Game.Barrel


class DonkeyKong(Entity):
    def __init__(self, entity_name: str, _pos: Vector3):
        # Base Constructor
        Entity.__init__(self, entity_name)
        self.transform.set_position(_pos)

        # Physics
        self.collision = self.add_component(Collider_AABB_2D(self.transform.get_position()))
        self.collision.offset = Vector2(0, 16)
        self.collision.type = Collision_Type.TRIGGER
        self.collision.id = Engine.Config.TRIGGER_ID_DEATH
        self.collision.size = Vector2(40, 32)
        # Animations
        self.animations = SpriteAnimation('anim_dk_frames')
        self.animations.set_speed(4.0)

        # Data
        self.pause_logic: bool = False
        self._barrel_count: int = 0
        self._barrels: List[Barrel] = []
        self._state: DK_State = DK_State_Still(self)

    def set_state(self, _new_state: DK_State_Enum):
        if self._state is not None:
            self._state.exit()

        self._state = Game.DonkeyKongState.create_state(self, _new_state)

        if self._state is not None:
            self._state.ID = _new_state
            self._state.enter()

    def set_frame(self, _index: int):
        self.animations.set_frame(_index)
        return self

    def get_total_barrel_count(self):
        return self._barrel_count

    def kill_all_barrels(self):
        for b in self._barrels:
            EntityManager.get_singleton().remove_entity(b)
        self._barrels.clear()

    def spawn_barrel(self, _state: Barrel_State = Barrel_State.RIGHT, _blue: bool = False):
        self._barrel_count += 1
        _barrel: Barrel = None

        # Regular Push
        if _state is Barrel_State.RIGHT:
            _barrel: Barrel = Barrel('barrel' + str(pygame.time.get_ticks()),
                                     self.transform.get_position() + Vector3(20, 0, 0), Barrel_State.RIGHT, _blue)

        # Regular Drop
        else:
            _barrel: Barrel = Barrel('barrel' + str(pygame.time.get_ticks()),
                                     self.transform.get_position() + Vector3(0, 0, 0), _state, _blue)

        # Spawn Debug
        # _barrel: Barrel = Barrel('barrel' + str(len(self._barrels)), Vector3(90, 30, 0), Barrel_State.LEFT)

        # Fix layer
        _barrel.set_layer(-1)
        EntityManager.get_singleton().add_entity(_barrel)

        self._barrels.append(_barrel)
        return self

    def update(self, delta_time):
        if self.pause_logic:
            return

        # Update State
        self._state.update(delta_time)

        # Update Barrel list
        _copy_barrels = self._barrels.copy()
        for b in _copy_barrels:
            if b.deleted is True:
                self._barrels.remove(b)

    def draw(self):
        self.animations.draw(self.transform)

    def draw_debug(self):
        self.collision.draw(Vector3(1, 0, 0))

# SpriteSequence('anim_dk_frames',
#                        'spr_dk_center',
#                        'spr_dk_left',
#                        'spr_dk_right',
#                        'spr_dk_hold_barrel1',
#                        'spr_dk_hold_barrel2',
#                        'spr_dk_drop'
#                        )

