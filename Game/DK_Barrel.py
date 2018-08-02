
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# DK from stage 1 that randomly throws barrels at given intervals

from Engine.Entity import *
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
import Engine.Config

class DK_Barrel(Entity_2D):
    def __init__(self, entity_name: str, _pos: Vector3):
        # Base Constructor
        Entity_2D.__init__(self, entity_name)
        self.transform.set_position(_pos)
        # Physics
        self.rigidbody = Rigidbody(self.transform.get_position())
        self.rigidbody.set_terminal_velocity_y(250)
        self.rigidbody.set_gravity(Vector3(0, -100, 0))
        # self.rigidbody.enabled = False
        self.collision = Collider_AABB_2D(self.transform.get_position())
        self.collision.offset = Vector2(0, 5)
        self.collision.type = Collision_Type.TRIGGER
        self.collision.id = Engine.Config.TRIGGER_ID_DEATH
        self._ray_left: Raycast_2D = None
        self._ray_right: Raycast_2D = None
        # Animations
        self.animations = SpriteAnimation('anim_barrel_roll')
        self.animations.set_speed(8.0)

        # Data
        self.h_speed_current: float = 0
        self.h_speed_move: float = 50
        self.h_speed_fall: float = 20
        self.direction = Direction.RIGHT

    def update(self, delta_time):
        _sprite = self.animations.get_current_frame()

        # Update Physics
        self.collision.set_size_from_sprite(self.transform, _sprite)
        self.rigidbody.update(delta_time)


    def draw(self):
        self.animations.draw(self.transform)
        self.collision.draw(Vector3(1, 0, 0))
