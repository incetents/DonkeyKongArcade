
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

class InvisBlock(Entity_2D):
    def __init__(self, entity_name: str, _pos: Vector3, _scale: Vector3):
        # Base Constructor
        Entity_2D.__init__(self, entity_name)
        self.transform.set_position(_pos)
        self.transform.set_scale(_scale)
        # Physics
        self.collision = Collider_AABB_2D(self.transform.get_position())
        self.collision.offset = Vector2(0, 16)
        self.collision.type = Collision_Type.SOLID
        self.collision.id = Engine.Config.TRIGGER_ID_WALL
        self.collision.size = self.transform.get_scale().get_vec2()
        # Data
        ColliderManager_2D.get_singleton().add_static_collider(self)

    def update(self, delta_time):
        pass

    def draw(self):
        self.collision.draw(Vector3(0, 1, 1))


