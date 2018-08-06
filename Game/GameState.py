
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Controls states of Game Class

# Math
import math
import Engine.Camera
import Engine.Collision
import Engine.Storage
import Engine.Input
import Engine.Config
from Engine.Storage import *
from Engine.Collision import *
from Engine.CollisionManager import *
from Engine.Raycast import *
from Engine.Vector import *
# Entities / Sprites
from Engine.Sprite import *
from Engine.Entity import *
from Engine.EntityManager import *
# Misc
from typing import List
import Engine.Graphics
import Engine.Config
# Game
import pygame
from Game.MarioState import *
from Game.Mario import *
from Game.Tile import *
from Game.Ladder import *
from Game.Enemy_Fire import *
from Game.Barrel import *
from Game.Oilbarrel import *
from Game.InvisBlock import *
from Game.DonkeyKong import *
# Text
from Engine.Text import *


ray: Raycast_2D = None

class GameState:
    def __init__(self):
        # Reset Collision System
        ColliderManager_2D.get_singleton().clear()
        # Reset Current List of Entities
        EntityManager_2D.get_singleton().clear()
        # Mario is global#
        self._mario: Mario = None
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        # Update Entities
        EntityManager_2D.get_singleton().update(delta_time)
        pass

    def draw(self):
        # Draw Entities
        EntityManager_2D.get_singleton().draw()
        pass

    def draw_ui(self, delta_time: float):
        pass


class GameState_Menu(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.test = Tile('dk', 'spr_barrel_stack1', Vector3())
        EntityManager_2D.get_singleton().add_entity(self.test)
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        super().update(delta_time)
        pass

    def draw(self):
        super().draw()
        pass

    def draw_ui(self, delta_time: float):
        pass


class GameState_Load(GameState):
    def __init__(self):
        GameState.__init__(self)
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        pass

    def draw(self):
        pass

    def draw_ui(self, delta_time: float):
        pass


class GameState_Game(GameState):
    def __init__(self):
        GameState.__init__(self)

        # Special Entities
        self._floor_tiles = TileBatch(
            'batch_tiles1', 'floor1', Collision_Type.PLATFORM)

        self._ladder_tiles = TileBatch(
            'batch_tiles2', 'ladder1', Collision_Type.TRIGGER, Engine.Config.TRIGGER_ID_LADDER)

        # Entities
        self._mario: Mario = Mario('mario')
        self._mario.transform.set_position(Vector3(50, 20, 2))
        self._mario.transform.set_flip_x(True)

        self._enemy1 = Enemy_Fire('enemy1', Vector3(120, 20, 0))

        self._barrel_1 = Barrel('barrel1', Vector3(80, 16, -2), Direction.LEFT)

        self._invis_box1 = InvisBlock('invis1', Vector3(-12, 92, 0), Vector3(8, 216, 1))
        self._invis_box2 = InvisBlock('invis2', Vector3(236, 92, 0), Vector3(8, 216, 1))

        self._oil1 = Oilbarrel('oil1', Vector3(24, 8, 0))

        self._destroy_barrel_trig = InvisBlock('trig_destroy_barrel',
                                               self._oil1.transform.get_position() + Vector3(-12, -8, 0),
                                               Vector3(16, 16, 1)
                                               )
        self._destroy_barrel_trig.collision.type = Collision_Type.TRIGGER
        self._destroy_barrel_trig.collision.id = Engine.Config.TRIGGER_ID_FIRE_BARREL

        self._stack_barrels = Tile('stack_o_barrels', 'spr_barrel_stack1', Vector3(0, 172, 0))
        self._stack_barrels.collision.offset = Vector2(10, 16)
        self._stack_barrels.collision.type = Collision_Type.TRIGGER
        self._stack_barrels.collision.id = Engine.Config.TRIGGER_ID_DEATH

        self._dk = DonkeyKong('dk', Vector3(42, 172, 0))

        # FLOORS
        ################
        # First Line
        self._floor_tiles.add_tile(Vector3(0, 0, 0), 'spr_floor_red_14')

        for i in range(7):
            self._floor_tiles.add_tile(Vector3(112 + (i * 16), i + 1, 0), 'spr_floor_red_2')

        # Backslash line 1
        for i in range(13):
            self._floor_tiles.add_tile(Vector3(16 * i, 40 - i, 0), 'spr_floor_red_2')

        # Forwardslash line 1
        for i in range(13):
            self._floor_tiles.add_tile(Vector3(16 * i + 16, 61 + i, 0), 'spr_floor_red_2')

        # Backslash line 2
        for i in range(13):
            self._floor_tiles.add_tile(Vector3(16 * i, 106 - i, 0), 'spr_floor_red_2')

        # Forwardslash line 2
        for i in range(13):
            self._floor_tiles.add_tile(Vector3(16 * i + 16, 127 + i, 0), 'spr_floor_red_2')

        # Last Line
        self._floor_tiles.add_tile(Vector3(0, 164, 0), 'spr_floor_red_18')

        for i in range(4):
            self._floor_tiles.add_tile(Vector3(16 * i + 144, 163 - i, 0), 'spr_floor_red_2')

        # Pauline Line
        self._floor_tiles.add_tile(Vector3(88, 192, 0), 'spr_floor_red_6')

        # LADDERS
        ################

        # DEBUG
        self._ladder_tiles.add_tile(Vector3(112, 9, 0), 'spr_ladder_24')

        # Ladder 1
        self._ladder_tiles.add_tile(Vector3(80, 8, 0), 'spr_ladder_8')
        self._ladder_tiles.add_tile(Vector3(80, 32, 0), 'spr_ladder_3')
        # Ladder 2
        self._ladder_tiles.add_tile(Vector3(184, 13, 0), 'spr_ladder_16')
        # Ladder 3
        self._ladder_tiles.add_tile(Vector3(96, 42, 0), 'spr_ladder_24')
        # Ladder 4
        self._ladder_tiles.add_tile(Vector3(32, 46, 0), 'spr_ladder_16')
        # Ladder 5
        self._ladder_tiles.add_tile(Vector3(64, 72, 0), 'spr_ladder_8')
        self._ladder_tiles.add_tile(Vector3(64, 96, 0), 'spr_ladder_6')
        # Ladder 6
        self._ladder_tiles.add_tile(Vector3(112, 75, 0), 'spr_ladder_24')
        # Ladder 7
        self._ladder_tiles.add_tile(Vector3(184, 79, 0), 'spr_ladder_16')
        # Ladder 8
        self._ladder_tiles.add_tile(Vector3(168, 104, 0), 'spr_ladder_8')
        self._ladder_tiles.add_tile(Vector3(168, 128, 0), 'spr_ladder_8')
        # Ladder 9
        self._ladder_tiles.add_tile(Vector3(72, 110, 0), 'spr_ladder_20')
        # Ladder 10
        self._ladder_tiles.add_tile(Vector3(32, 112, 0), 'spr_ladder_16')
        # Ladder 11
        self._ladder_tiles.add_tile(Vector3(88, 139, 0), 'spr_ladder_13')
        self._ladder_tiles.add_tile(Vector3(88, 160, 0), 'spr_ladder_3')
        # Ladder 12
        self._ladder_tiles.add_tile(Vector3(184, 145, 0), 'spr_ladder_16')
        # Ladder 13
        self._ladder_tiles.add_tile(Vector3(128, 172, 0), 'spr_ladder_20')
        # Ladder DK
        self._ladder_tiles.add_tile(Vector3(64, 172, 0), 'spr_ladder_52')
        self._ladder_tiles.add_tile(Vector3(80, 172, 0), 'spr_ladder_52')

        pass

    def enter(self):
        # Add entities
        # EntityManager_2D.get_singleton().add_entity(self._enemy1)
        EntityManager_2D.get_singleton().add_entity(self._invis_box1)
        EntityManager_2D.get_singleton().add_entity(self._invis_box2)
        EntityManager_2D.get_singleton().add_entity(self._oil1)
        EntityManager_2D.get_singleton().add_entity(self._destroy_barrel_trig)
        EntityManager_2D.get_singleton().add_entity(self._stack_barrels)
        EntityManager_2D.get_singleton().add_entity(self._dk)
        # EntityManager_2D.get_singleton().add_entity(self._barrel_1)

        EntityManager_2D.get_singleton().add_batch(self._floor_tiles)
        EntityManager_2D.get_singleton().add_batch(self._ladder_tiles)

        EntityManager_2D.get_singleton().add_entity(self._mario)
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        # Base
        #print('~~~')
        #_t = pygame.time.get_ticks()
        super().update(delta_time)
        #print('update time:', pygame.time.get_ticks() - _t)

        # Debug Mode
        if Engine.Input.get_key(pygame.K_n):
            self._mario.debug = True
        if Engine.Input.get_key(pygame.K_m):
            self._mario.debug = False

        # TEST
        if Engine.Input.get_key_pressed(pygame.K_z):
            self._dk.spawn_barrel()
            # self._oil1.spawn_fire()

        # Test
        if Engine.Input.get_key(pygame.K_q):
            self._mario.set_state(MarioState_Enum.DEAD)


        # ------------------------------------------

    def draw(self):
        # Base
        # print('~~~')
        # _t = pygame.time.get_ticks()
        super().draw()
        # print('draw time:', pygame.time.get_ticks() - _t)

        # Chunk outlines
        _c = ColliderManager_2D.get_singleton()
        _c.draw_chunks()

        # ------------------------------------------

    def draw_ui(self, delta_time: float):
        # Data
        _fps: str = '0'
        if delta_time > 0.0:
            _fps = str(round(100.0 / delta_time) / 100.0)

        _camerapos = str(Engine.Camera.position)
        _camerazoom = str(round(Engine.Camera.zoom * 100.0) / 100.0)
        _playerpos = str(round(self._mario.transform.get_position() * 10.0) / 10.0)

        _text = Text(
            'FPS: ' + _fps + '\nCamera Pos: ' + _camerapos + '\nCameraZoom: ' + _camerazoom +
            '\nMario Pos: ' + _playerpos,
            Vector2(-Engine.Config.SCREEN_WIDTH / 2 + 5, +Engine.Config.SCREEN_HEIGHT / 2 - 30),
            38,
            Vector4(0.9, 0.8, 0.88, 1),
            TextAlignment.LEFT,
            48,
            0.5
        )

        _text.draw()
        # ------------------------------------------
