
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Oil Barrel is a kill zone that spawns fire

import pygame
from Engine.Entity import *
from Engine.EntityManager import *
from Engine.Sprite import *
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
from Game.Enemy_Fire import *
from Engine.Clock import *
from Engine.SpriteBatch import *


class Oilbarrel(Entity):
    def __init__(self, entity_name: str, _pos: Vector3):
        # Base Constructor
        Entity.__init__(self, entity_name)
        self.transform.set_position(_pos)
        # Physics
        self.collision = self.add_component(Collider_AABB_2D(self.transform.get_position()))
        self.collision.offset = Vector2(0, 16)
        self.collision.type = Collision_Type.TRIGGER
        self.collision.id = Engine.Config.TRIGGER_ID_DEATH
        self._ray_left: Raycast_2D = None
        self._ray_right: Raycast_2D = None
        # Animations
        self.animations = SpriteAnimation('anim_oil_barrel_empty')
        self.animations.set_speed(8.0)

        # Data
        self._fire: Enemy_Fire = None

    def spawn_fire(self):
        # append time to created fire to make sure its unique
        if self._fire is not None:
            EntityManager_2D.get_singleton().remove_entity(self._fire)

        self._fire = Enemy_Fire('new_fire', self.transform.get_position() + Vector3(0, 20.0, 0))
        self._fire.rigidbody.set_velocity(Vector3(20, 40, 0))

        EntityManager_2D.get_singleton().add_entity(self._fire)


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

