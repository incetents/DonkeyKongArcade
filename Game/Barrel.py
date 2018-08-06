
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Barrel has a bit of complexity,
# can be moving left or right normally, go down ladders
# or it can fall from its spawn position from donkey kong

from Engine.Entity import *
from Engine.EntityManager import *
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
import Engine.Collision
import Engine.Config

class Barrel(Entity):
    def __init__(self, entity_name: str, _pos: Vector3, _direction: Direction=Direction.RIGHT):
        # Base Constructor
        Entity.__init__(self, entity_name)
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
        self.direction = _direction

    def update(self, delta_time):
        _sprite = self.animations.get_current_frame()

        # Update Physics
        self.collision.set_size_from_sprite(self.transform, _sprite)
        self.rigidbody.update(delta_time)

        # Raycast to see if anything below barrel
        self._bottom_left_anchor = _sprite.get_anchor(Anchor.BOTLEFT, self.transform) + Vector2(0, 0.2)
        self._bottom_right_anchor = _sprite.get_anchor(Anchor.BOTRIGHT, self.transform) + Vector2(0, 0.2)

        # print('~~~')#
        # _t = pygame.time.get_ticks()
        self._ray_left = Raycast_2D(self._bottom_left_anchor, Vector2(0, -1), 5, True)
        self._ray_right = Raycast_2D(self._bottom_right_anchor, Vector2(0, -1), 5, True)
        # print('raycast time for:', self.name, pygame.time.get_ticks() - _t)

        # Update Ground Data
        self.above_emptiness = \
            (self._ray_left.hit_distance > 2.5 or self._ray_left.hit_flag is False) and \
            (self._ray_right.hit_distance > 2.5 or self._ray_right.hit_flag is False)

        if self.above_emptiness is True:
            self.h_speed_current = self.h_speed_fall
        else:
            self.h_speed_current = self.h_speed_move

        if self.direction is Direction.LEFT:
            self.animations.update(-delta_time * (0.0 if self.above_emptiness is True else 1.0))
            self.rigidbody.set_vel_x(-self.h_speed_current)
        elif self.direction is Direction.RIGHT:
            self.animations.update(+delta_time * (0.0 if self.above_emptiness is True else 1.0))
            self.rigidbody.set_vel_x(+self.h_speed_current)

    def draw(self):
        self.animations.draw(self.transform)
        self.collision.draw(Vector3(1, 0, 0))

        # Draw Raycast Stuff
        # if self._ray_right is not None and self._ray_left is not None:
        #     Debug.draw_circle_2d(self._bottom_left_anchor, 1.0, Vector3(0, 1, 0))
        #     Debug.draw_circle_2d(self._bottom_right_anchor, 1.0, Vector3(0, 1, 0))
        #     Debug.draw_line_2d(
        #         self._bottom_left_anchor,
        #         self._ray_left.ray_end,
        #         Vector3(1, 0, 0)
        #     )
        #     Debug.draw_line_2d(
        #         self._bottom_right_anchor,
        #         self._ray_right.ray_end,
        #         Vector3(1, 0, 0)
        #     )
        #     if self._ray_left.hit_flag is not False:
        #         Debug.draw_circle_2d(self._ray_left.hit_point, 2.0, Vector3(0,1,0))
        #     if self._ray_right.hit_flag is not False:
        #         Debug.draw_circle_2d(self._ray_right.hit_point, 2.0, Vector3(0,1,0))

    def collider_enter(self, collider: Collider):
        if collider.id is Engine.Config.TRIGGER_ID_WALL:
            if self.direction is Direction.RIGHT:
                self.direction = Direction.LEFT
            else:
                self.direction = Direction.RIGHT

    def trigger_enter(self, trigger: Collider):
        if trigger.id is Engine.Config.TRIGGER_ID_FIRE_BARREL:
            EntityManager_2D.get_singleton().remove_entity(self)
        pass