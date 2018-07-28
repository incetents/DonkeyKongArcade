
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Main Game Functionality Goes Here]

import pygame

# Textures
from Engine.Texture import *
# Sprites
from Engine.Sprite import *
# Math
import math
import Engine.Camera
from Engine.Vector import *
from Engine.Collision import *
from Engine.Transform import *
import Engine.Collision
from Engine.CollisionManager import *
from Engine.Rigidbody import *
# Data
import Engine.Input
import Engine.Storage
from Engine.Text import *

from Engine.Graphics import *

# Entities
from Engine.Entity import *
from Game.Mario import *
from Game.Tile import *


# Misc
from typing import List
from OpenGL.GL import *
import Engine.Config
from Game.GameState import *

_instance = None

class Game:
    def __init__(self):
        # State
        self._state = GameState()
        # Setup Functions
        self.setup_systems()
        self.setup_textures()
        self.setup_sprites()
        self.setup_animations()
        self.setup_meshes()
        # Initial State
        self.set_state(GameState_Game())

    @staticmethod
    def get_singleton():
        global _instance
        if _instance is None:
            _instance = Game()
        return _instance

    def set_state(self, _new_state: GameState):
        self._state.exit()
        # Reset Collision System
        ColliderManager_2D.get_singleton().clear()

        self._state = _new_state
        self._state.enter()

    def get_state(self) -> GameState:
        return self._state

    def setup_systems(self):
        # Setup Core Systems
        pass

    def setup_textures(self):
        # Load Textures
        Texture('font', 'assets/text/tilesheet.png', FilterMode.POINT, WrapMode.CLAMP)

        Texture('dk1', 'assets/dk/dk1.png', FilterMode.POINT, WrapMode.CLAMP)

        Texture('mario1',     'assets/mario/mario1.png',     FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario2',     'assets/mario/mario2.png',     FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario3',     'assets/mario/mario3.png',     FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_jump', 'assets/mario/mario_jump.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_death1', 'assets/mario/mario_death1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_death2', 'assets/mario/mario_death2.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_dead', 'assets/mario/mario_dead.png', FilterMode.POINT, WrapMode.CLAMP)

        Texture('floor1', 'assets/tiles/floor1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('ladder1', 'assets/tiles/ladder1.png', FilterMode.POINT, WrapMode.CLAMP)

        Texture('fire1', 'assets/enemies/fire1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire2', 'assets/enemies/fire2.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire3', 'assets/enemies/fire3.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire_blue1', 'assets/enemies/fire_blue1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire_blue2', 'assets/enemies/fire_blue2.png', FilterMode.POINT, WrapMode.CLAMP)

    def setup_sprites(self):
        # Load Sprites
        Sprite('spr_dk1', 'dk1')

        Sprite('spr_mario1', 'mario1')
        Sprite('spr_mario2', 'mario2')
        Sprite('spr_mario3', 'mario3')
        Sprite('spr_mario_jump', 'mario_jump')
        Sprite('spr_mario_death1', 'mario_death1')
        Sprite('spr_mario_death2', 'mario_death2')
        Sprite('spr_mario_death3', 'mario_death1').set_flip_y(True)
        Sprite('spr_mario_death4', 'mario_death2').set_flip_x(True)
        Sprite('spr_mario_dead', 'mario_dead')

        Sprite('spr_floor1', 'floor1')
        Sprite('spr_ladder1', 'ladder1')

        Sprite('spr_enemy_fire1', 'fire1')
        Sprite('spr_enemy_fire2', 'fire2')

    def setup_animations(self):
        # Load Animations
        SpriteSequence('anim_mario_idle',
                        'spr_mario1'
                        )
        SpriteSequence('anim_mario_walk',
                        'spr_mario1',
                        'spr_mario2',
                        'spr_mario2',
                        'spr_mario1',
                        'spr_mario3',
                        'spr_mario3'
                        )
        SpriteSequence('anim_mario_jump',
                        'spr_mario_jump'
                        )
        SpriteSequence('anim_mario_dying',
                        'spr_mario_death1',
                        'spr_mario_death2',
                        'spr_mario_death3',
                        'spr_mario_death4'
                        )
        SpriteSequence('anim_mario_dead',
                        'spr_mario_dead'
                        )

        SpriteSequence('anim_enemy1',
                       'spr_enemy_fire2',
                       'spr_enemy_fire2'
                       )

    def setup_meshes(self):
        # Load Meshes
        _m1 = Mesh('quad_2d')

        _v = (
            Vector3(-0.5, -0.5, 0),
            Vector3(+0.5, -0.5, 0),
            Vector3(+0.5, +0.5, 0),
            Vector3(-0.5, +0.5, 0)
        )
        _uv = (
            Vector2(0, 0),
            Vector2(1, 0),
            Vector2(1, 1),
            Vector2(0, 1)
        )

        _m1.set_vertices(_v)
        _m1.set_uvs(_uv)

    def update(self, delta_time: float):

        # State Update
        self._state.update(delta_time)

        # Move Camera
        if Engine.Input.get_key(pygame.K_w):
            Engine.Camera.move_up()
        elif Engine.Input.get_key(pygame.K_s):
            Engine.Camera.move_down()
        if Engine.Input.get_key(pygame.K_a):
            Engine.Camera.move_left()
        elif Engine.Input.get_key(pygame.K_d):
            Engine.Camera.move_right()

        if Engine.Input.get_key(pygame.K_z):
            Engine.Camera.zoom_in()
        elif Engine.Input.get_key(pygame.K_x):
            Engine.Camera.zoom_out()

        # Mode Switcher
        if Engine.Input.get_key(pygame.K_1):
            self.set_state(GameState_Menu())
        elif Engine.Input.get_key(pygame.K_2):
            self.set_state(GameState_Game())


    def draw(self):

        Engine.Camera.push()

        # State Draw
        self._state.draw()

        Debug.draw_line(Vector3(-120, -120, 0), Vector3(320, 320, 0), Vector3(1, 0, 0))
        Debug.draw_line(Vector3(0, -200, 0), Vector3(0, 200, 0), Vector3(1, 1, 0))
        Debug.draw_line(Vector3(-200, 0, 0), Vector3(200, 0, 0), Vector3(0, 0, 1))

        Engine.Camera.pop()
        glFlush()

    def draw_UI(self, delta_time):

        # Draw UI
        self._state.draw_ui(delta_time)




        pass