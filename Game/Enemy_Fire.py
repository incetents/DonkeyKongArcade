
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Enemy fire guy that slowly follows mario and kills on hit

import Engine.Input
from Engine.Entity import *
from Engine.Sprite import *
import pygame
from Game.MarioState import *
import Game.MarioState
# Math
from Engine.Vector import *
# Physics
from Engine.Rigidbody import *
from Engine.Collision import *
from Engine.Clock import *
from Engine.EntityManager import *
import Engine.Config
from Game.Mario import *
from Game.TriggerZone import *


class Enemy_Fire(Entity):
    def __init__(self, entity_name: str, _position: Vector3):
        # Base Constructor
        Entity.__init__(self, entity_name)
        self.transform.set_position(_position)
        # Physics
        self.rigidbody = self.add_component(Rigidbody(self.transform.get_position()))
        self.rigidbody.set_terminal_velocity_y(250)
        self.rigidbody.set_gravity(Vector3(0, -100, 0))
        self.rigidbody.ignore_dynamic_colliders = True
        self.collision: Collider_AABB_2D = self.add_component(Collider_AABB_2D(self.transform.get_position()))
        self.collision.type = Collision_Type.TRIGGER
        self.collision.id = Engine.Config.TRIGGER_ID_FLAME
        # Animations
        self.animations = SpriteAnimation('anim_enemy1')
        self.animations.set_speed(10.0)

        # Create Trigger Zone on self
        _trigger: TriggerZone = TriggerZone('trig_fire' + str(pygame.time.get_ticks()), self,
                                            Engine.Config.TRIGGER_ID_SCORE_DEATH,
                                            Vector2(4, 20), Vector2(0, 4)
                                            )
        EntityManager.get_singleton().add_entity(_trigger)


        # Data
        self.speed: float = 5

    def update(self, delta_time):

        self.animations.update(delta_time)
        _sprite = self.animations.get_current_frame()

        # Update Physics
        self.collision.set_size_from_sprite(self.transform, _sprite)
        self.collision.size = self.collision.size.mult(Vector2(0.75, 0.5))
        self.collision.offset = Vector2(0, -4)
        self.rigidbody.update(delta_time)

        # Simple AI (Move Towards Mario)
        _mario = Game.Game._instance.get_singleton().get_Mario()
        # _m: Mario = Game.get_singleton().get_Mario()
        # if self.transform.get_position().x < _m.transform.get_position().x:
        #     self.rigidbody.set_velocity(Vector3(+self.speed, 0, 0))
        # else:
        #     self.rigidbody.set_velocity(Vector3(-self.speed, 0, 0))

        # Kill Condition
        # if self.transform.get_position().y < - 5.0:
        #     print('fart')
        #     EntityManager.get_singleton().remove_entity(self)

    def draw(self):
        self.animations.draw(self.transform)

    def draw_debug(self):
        self.collision.draw(Vector3(1, 0, 0))
