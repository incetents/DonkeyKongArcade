
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Oil Barrel is a kill zone that spawns fire

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
# Misc
from Engine.Anchor import *

class Oilbarrel(Entity_2D):
    def __init__(self, entity_name: str, _pos: Vector3):
        # Base Constructor
        Entity_2D.__init__(self, entity_name)
        self.transform.set_position(_pos)
        # Physics
        self.collision = Collider_AABB_2D(self.transform.get_position())
        self.collision.offset = Vector2(0, 16)
        self.collision.type = Collision_Type.TRIGGER
        self.collision.id = Engine.Config.TRIGGER_ID_DEATH
        self._ray_left: Raycast_2D = None
        self._ray_right: Raycast_2D = None
        # Animations
        self.animations = SpriteAnimation('anim_oil_barrel_empty')
        self.animations.set_speed(8.0)
        # Data
        ColliderManager_2D.get_singleton().add_static_collider(self)


    def update(self, delta_time):
        self.animations.update(delta_time)
        _sprite = self.animations.get_current_frame()

        # Update Physics
        self.collision.set_size_from_sprite(self.transform, _sprite)
        self.collision.size *= 0.5

    def draw(self):
        self.animations.draw(self.transform)
        self.collision.draw(Vector3(1, 0, 0))

        _pos = self.transform.get_position().get_vec2()

        Debug.draw_x_2d(_pos, 5.0, Vector3(1, 1, 0))

