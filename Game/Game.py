
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
from Engine.Anchor import *
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

        Texture('pixel_black', 'assets/pixels/pixel_black.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('pixel_white', 'assets/pixels/pixel_white.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('pixel_red', 'assets/pixels/pixel_red.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('pixel_green', 'assets/pixels/pixel_green.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('pixel_blue', 'assets/pixels/pixel_blue.png', FilterMode.POINT, WrapMode.CLAMP)

        Texture('dk_center', 'assets/dk/dk1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('dk_left', 'assets/dk/dk2.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('dk_drop', 'assets/dk/dk3.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('dk_pound', 'assets/dk/dk4.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('dk_climb1', 'assets/dk/dk5.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('dk_climb2', 'assets/dk/dk6.png', FilterMode.POINT, WrapMode.CLAMP)

        Texture('mario1',     'assets/mario/mario1.png',     FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario2',     'assets/mario/mario2.png',     FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario3',     'assets/mario/mario3.png',     FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_jump', 'assets/mario/mario_jump.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_death1', 'assets/mario/mario_death1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_death2', 'assets/mario/mario_death2.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_dead', 'assets/mario/mario_dead.png', FilterMode.POINT, WrapMode.CLAMP)

        Texture('floor1', 'assets/tiles/floor1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('ladder1', 'assets/tiles/ladder1.png', FilterMode.POINT, WrapMode.CLAMP)

        Texture('barrel_side1', 'assets/objects/barrel_side1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('barrel_side2', 'assets/objects/barrel_side2.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('barrel', 'assets/objects/barrel.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('barrel_vertical', 'assets/objects/barrel_vertical.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('barrel_stack', 'assets/objects/stacked_barrels.png', FilterMode.POINT, WrapMode.CLAMP)

        Texture('fire_barrel1', 'assets/enemies/fire_barrel1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire_barrel2', 'assets/enemies/fire_barrel2.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire_barrel3', 'assets/enemies/fire_barrel3.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire_barrel4', 'assets/enemies/fire_barrel4.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire_barrel5', 'assets/enemies/fire_barrel5.png', FilterMode.POINT, WrapMode.CLAMP)

        Texture('fire1', 'assets/enemies/fire1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire2', 'assets/enemies/fire2.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire_blue1', 'assets/enemies/fire_blue1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire_blue2', 'assets/enemies/fire_blue2.png', FilterMode.POINT, WrapMode.CLAMP)

    def setup_sprites(self):
        # Load Sprites
        Sprite('spr_pixel_black', 'pixel_black')
        Sprite('spr_pixel_white', 'pixel_white')
        Sprite('spr_pixel_red', 'pixel_red')
        Sprite('spr_pixel_green', 'pixel_green')
        Sprite('spr_pixel_blue', 'pixel_blue')

        Sprite('spr_dk_center', 'dk_center', Anchor.BOT)
        Sprite('spr_dk_left', 'dk_left', Anchor.BOT)
        Sprite('spr_dk_right', 'dk_left', Anchor.BOT).set_flip_x(True)
        Sprite('spr_dk_drop', 'dk_drop', Anchor.BOT)

        Sprite('spr_mario1', 'mario1', Anchor.BOT)
        Sprite('spr_mario2', 'mario2', Anchor.BOT)
        Sprite('spr_mario3', 'mario3', Anchor.BOT)
        Sprite('spr_mario_jump', 'mario_jump', Anchor.BOT)
        Sprite('spr_mario_death1', 'mario_death1', Anchor.BOT)
        Sprite('spr_mario_death2', 'mario_death2', Anchor.BOT)
        Sprite('spr_mario_death3', 'mario_death1', Anchor.BOT).set_flip_y(True)
        Sprite('spr_mario_death4', 'mario_death2', Anchor.BOT).set_flip_x(True)
        Sprite('spr_mario_dead', 'mario_dead', Anchor.BOT)

        Sprite('spr_floor1', 'floor1', Anchor.BOTLEFT)
        Sprite('spr_ladder1', 'ladder1', Anchor.BOTLEFT)

        Sprite('spr_fire_barrel1', 'fire_barrel1', Anchor.BOT)
        Sprite('spr_fire_barrel2', 'fire_barrel2', Anchor.BOT)
        Sprite('spr_fire_barrel3', 'fire_barrel3', Anchor.BOT)
        Sprite('spr_fire_barrel4', 'fire_barrel4', Anchor.BOT)
        Sprite('spr_fire_barrel5', 'fire_barrel5', Anchor.BOT)

        Sprite('spr_barrel_side1', 'barrel_side1', Anchor.BOT)
        Sprite('spr_barrel_side2', 'barrel_side2', Anchor.BOT)
        Sprite('spr_barrel_1', 'barrel', Anchor.BOT)
        Sprite('spr_barrel_2', 'barrel', Anchor.BOT).set_flip_x(True)
        Sprite('spr_barrel_3', 'barrel', Anchor.BOT).set_flip_x(True).set_flip_y(True)
        Sprite('spr_barrel_4', 'barrel', Anchor.BOT).set_flip_y(True)
        Sprite('spr_barrel_vertical', 'barrel_vertical')
        Sprite('spr_barrel_stack1', 'barrel_stack', Anchor.BOTLEFT)

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

        SpriteSequence('anim_oil_barrel_empty',
                       'spr_fire_barrel1',
                       'spr_fire_barrel2'
                       )

        SpriteSequence('anim_oil_barrel_burn',
                       'spr_fire_barrel3',
                       'spr_fire_barrel4',
                       )

        SpriteSequence('anim_barrel_roll',
                       'spr_barrel_1',
                       'spr_barrel_2',
                       'spr_barrel_3',
                       'spr_barrel_4'
                       )

        SpriteSequence('anim_enemy1',
                       'spr_enemy_fire1',
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
            Engine.Camera.zoom_out()#

        # Mode Switcher
        if Engine.Input.get_key(pygame.K_1):
            self.set_state(GameState_Menu())
        elif Engine.Input.get_key(pygame.K_2):
            self.set_state(GameState_Game())


    def draw(self):
        Engine.Camera.push()

        # State Draw
        self._state.draw()

        Engine.Camera.pop()
        glFlush()

    def draw_UI(self, delta_time):

        # Draw UI
        self._state.draw_ui(delta_time)




        pass