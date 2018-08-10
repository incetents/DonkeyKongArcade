
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Mario Character]

from Engine.Entity import *
from Engine.Sprite import *
import Engine.Input
import Engine.Raycast
import pygame
import Engine.Storage
from Game.MarioState import *
import Game.MarioState
from Game.Tile import *
from Game.Barrel import *
# Math
from Engine.Vector import *
# Physics
from Engine.Rigidbody import *
from Engine.Collision import *
from Engine.CollisionManager import *
from Engine.Raycast import *
from Engine.Anchor import *
from Engine.AudioPlayer import *

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
        self.collision: Collider_AABB_2D = self.add_component(Collider_AABB_2D(self.transform.get_position()))
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
        self.touching_ground: bool = False
        self.barrel_count: int = 0
        self.barrel_combo: int = 0
        self.barrel_score: int = 0
        self.x_distance_to_ladder_for_climb: float = 4.0
        self._ladder_ref: Tile = None
        self._bottom_left_anchor: Vector2 = Vector2()
        self._bottom_right_anchor: Vector2 = Vector2()
        # Audio
        self.sfx_jump: SFX = Engine.Storage.get(Engine.Storage.Type.SFX, 'sfx_jump')

        self.sfx_walk1: SFX = Engine.Storage.get(Engine.Storage.Type.SFX, 'sfx_walk1')
        self.sfx_walk2: SFX = Engine.Storage.get(Engine.Storage.Type.SFX, 'sfx_walk2')
        self.sfx_walk3: SFX = Engine.Storage.get(Engine.Storage.Type.SFX, 'sfx_walk3')
        self.sfx_walk4: SFX = Engine.Storage.get(Engine.Storage.Type.SFX, 'sfx_walk4')
        self.sfx_walk5: SFX = Engine.Storage.get(Engine.Storage.Type.SFX, 'sfx_walk5')

        self.sfx_walks = [self.sfx_walk1, self.sfx_walk2, self.sfx_walk3, self.sfx_walk4, self.sfx_walk5]
        self.sfx_walk_index: int = -1

        self.sfx_barrel_score: SFX = Engine.Storage.get(Engine.Storage.Type.SFX, 'sfx_barrel_score')


    def get_random_walk_sfx(self):
        _rand: int = randint(0, len(self.sfx_walks) - 1)
        # Prevent same clip twice
        if _rand is self.sfx_walk_index:
            _rand = (_rand + 1) % (len(self.sfx_walks) - 1)
        # Return
        return self.sfx_walks[_rand]

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
        self.collision.size.x *= 0.75
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
        # _cols: List[Entity] = Engine.Raycast.Raypoint_2D_Static_Static(self.transform.get_position().get_vec2())
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
        # Ignore future logic if dead
        if not self.alive:
            return

        # Death Trigger
        if not self._debug and \
                (trigger.id is Engine.Config.TRIGGER_ID_DEATH or
                 trigger.id is Engine.Config.TRIGGER_ID_OIL_BARREL or
                 trigger.id is Engine.Config.TRIGGER_ID_FLAME
                ):
            self.set_state(MarioState_Enum.DEAD)

        # Special Barrel Trigger
        if trigger.id is Engine.Config.TRIGGER_ID_BARREL_SPECIAL:
            if self.transform.get_position().y > trigger.get_position().y - 2:
                # Barrel Counter
                self.barrel_count += 1
                self.barrel_combo += 1
                # Audio
                self.sfx_barrel_score.play()
            else:
                self.set_state(MarioState_Enum.DEAD)

        # Ladder Exception
        if self._debug is False and trigger.id is Engine.Config.TRIGGER_ID_BARREL and \
                self._state.ID is MarioState_Enum.CLIMB:
            self.set_state(MarioState_Enum.DEAD)

        pass

    def trigger_exit(self, trigger: Collider):
        # Special Barrel Trigger
        if trigger.id is Engine.Config.TRIGGER_ID_BARREL_SPECIAL:
            if self.transform.get_position().y > trigger.get_position().y - 2:
                # Barrel Counter
                self.barrel_count -= 1
                # If reached 0, calculate score
                if self.barrel_count is 0:
                    # Get correct sprite
                    spr_name: str = 'spr_score_100'
                    self.barrel_score += 100
                    if self.barrel_combo is 2:
                        spr_name = 'spr_score_300'
                        self.barrel_score += 200
                    elif self.barrel_combo > 2:
                        spr_name = 'spr_score_500'
                        self.barrel_score += 400

                    # Spawn Effect
                    _score = BarrelScore(
                        'barrel_score' + str(pygame.time.get_ticks()),
                        Vector3(self.transform.get_position().x, trigger.get_position().y, 2),
                        spr_name
                    )
                    EntityManager.get_singleton().add_entity(_score)

                    # Reset Combo
                    self.barrel_combo = 0
        pass


