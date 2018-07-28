
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Enemy fire guy that slowly follows mario and kills on hit

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

class Enemy_Fire(Entity_2D):
    def __init__(self, entity_name: str):
        # Base Constructor
        Entity_2D.__init__(self, entity_name)
        # Physics
        self.rigidbody = Rigidbody(self.transform.get_position())
        self.collision = Collider_AABB_2D(self.transform.get_position())
        self.collision.type = Collision_Type.TRIGGER
        self.collision.id = Engine.Config.TRIGGER_ID_DEATH
        self.collision.enabled = False
        # Animations
        self.animations = SpriteAnimation('anim_enemy1')
        self.animations.set_speed(8.0)

    def update(self, delta_time):
        self.animations.update(delta_time)
        _sprite = self.animations.get_current_frame()

        # Update Physics
        self.collision.update_size_from_sprite(self.transform, _sprite)
        self.rigidbody.update(delta_time)

    def draw(self):
        self.animations.draw(self.transform)
        self.collision.draw(Vector3(1, 0, 0))